from fastapi import APIRouter, Response
import json
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.schemas import PontuacaoSchema
from sqlalchemy import select
from src.models.models import Pontuacoes, Ranking
from src.database.db_connection import async_session
import asyncpg
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from src.services.PontuacaoService import PontuacaoService
from sqlalchemy import text

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = getenv('DATABASE_URL')

async def connect_to_db():
    async with async_session() as session:
        return session

async def close_db_connection(session):
    await session.close()

pontuacao_router = APIRouter(prefix='/pontuacao', tags=['Pontuação'])

@pontuacao_router.post('/create_pontuacao', response_model=PontuacaoSchema.StandardOutput, responses={400: {'model': PontuacaoSchema.ErrorOutput}})
async def create_pontuacao(pontuacao: PontuacaoSchema.PontuacaoInput):
    try:
        await PontuacaoService.create_pontuacao(
            pontuacao
        )
        return PontuacaoSchema.StandardOutput(message='Success')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@pontuacao_router.get('/get_pontuacao', response_model=PontuacaoSchema.StandardOutput, responses={400: {'model': PontuacaoSchema.ErrorOutput}})
async def notas_pontuacao():
    notas_competidores = []

    try:
        async with async_session() as session:
            query = text("""
            SELECT
                c.apelido AS competidor,
                c.numero AS numero,
                c.sexo AS sexo,
                ca.nome AS categoria,
                fase,
                p.id_competidor,
                SUM(p.nota_total_jogo) AS total_jogo,
                SUM(p.nota_total_competidor) AS total_competidor,
                SUM(p.nota_geral_competidor) AS nota_total
            FROM (
                SELECT
                    id_competidor,
                    id_categoria,
                    fase,
                    SUM(nota_total_jogo) AS nota_total_jogo,
                    SUM(nota_total_competidor) AS nota_total_competidor,
                    SUM(nota_total_competidor + nota_total_jogo) AS nota_geral_competidor
                FROM (
                    SELECT
                        j.id_competidor_1 AS id_competidor,
                        j.id_categoria,
                        j.fase,
                        SUM(p.pontuacao_jogo) AS nota_total_jogo,
                        SUM(p.pontuacao_competidor_1) AS nota_total_competidor
                    FROM
                    "Jogos" j
                    JOIN
                    "Pontuacoes" p ON p.id_jogo = j.id
                GROUP BY
                    j.id_competidor_1, j.id_categoria, j.fase, p.id_jogo
                HAVING
                    COUNT(p.pontuacao_jogo) = 3

            UNION ALL

            SELECT
                j.id_competidor_2 AS id_competidor,
                j.id_categoria,
                j.fase,
                SUM(p.pontuacao_jogo) AS nota_total_jogo,
                SUM(p.pontuacao_competidor_2) AS nota_total_competidor
            FROM
                "Jogos" j
            JOIN
                "Pontuacoes" p ON p.id_jogo = j.id
            GROUP BY
                j.id_competidor_2, j.id_categoria, j.fase, p.id_jogo
            HAVING
                COUNT(p.pontuacao_jogo) = 3
            ) AS notas_por_jogo
            GROUP BY
                id_competidor, id_categoria, fase
            ) AS p
            JOIN
                "Competidores" c ON c.id = p.id_competidor
            JOIN
                "Categorias" ca ON ca.id = p.id_categoria
            GROUP BY
                c.apelido, ca.nome, c.sexo, c.numero, p.id_competidor, fase
            ORDER BY
                ca.nome, nota_total DESC, c.apelido;
            """)

            result = await session.execute(query)
            competidores = result.fetchall()

        for row in competidores:
            notas_competidores.append({
                "competidor": row[0],
                "numero": row[1],
                "sexo": row[2],
                "categoria": row[3],
                "fase": row[4],
                "id_competidor": str(row[5]),
                "total_jogo": row[6],
                "total_competidor": row[7],
                "nota_total": row[8]
            })

        content = {
            "notas": notas_competidores
        }

        for nota in notas_competidores:
            existing_ranking = await session.execute(
                select(Ranking).where(
                    (Ranking.fase == nota["fase"]) & (Ranking.id_competidor == nota["id_competidor"])
                )
            )
            existing_ranking = existing_ranking.scalar_one_or_none()

            if existing_ranking is not None:
                continue 

            new_ranking = Ranking(
                apelido=nota["competidor"],
                numero=nota["numero"],
                sexo=nota["sexo"],
                categoria=nota["categoria"],
                fase=nota["fase"],
                id_competidor=nota["id_competidor"],
                total_jogo=nota["total_jogo"],
                total_competidor=nota["total_competidor"],
                nota_total=nota["nota_total"]
            )
            session.add(new_ranking)

        await session.commit()
    
    finally:
        await session.close()

    return JSONResponse(content=content)