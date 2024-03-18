from fastapi import APIRouter, Response
import json
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.schemas import PontuacaoSchema
from src.models.models import Pontuacoes
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

    async with async_session() as session:
        query = text("""
        SELECT
            c.nome AS nome_competidor,
            p.id_competidor,
            SUM(p.nota_total_jogo) AS total_jogo,
            SUM(p.nota_total_competidor) AS total_competidor,
            SUM(p.nota_geral_competidor) AS nota_total
        FROM (
            SELECT
                id_jogo,
                id_competidor,
                nota_total_competidor,
                nota_total_jogo,
                nota_geral_competidor
            FROM (
                SELECT
                    j.id AS id_jogo,
                    j.id_competidor_1 AS id_competidor,
                    SUM(p.pontuacao_jogo) AS nota_total_jogo,
                    SUM(p.pontuacao_competidor_1) AS nota_total_competidor,
                    SUM(p.pontuacao_competidor_1 + p.pontuacao_jogo) AS nota_geral_competidor
                FROM
                    "Jogos" j
                JOIN
                    "Pontuacoes" p ON p.id_jogo = j.id
                GROUP BY
                    j.id, j.id_competidor_1

                UNION ALL

                SELECT
                    j.id AS id_jogo,
                    j.id_competidor_2 AS id_competidor,
                    SUM(p.pontuacao_jogo) AS nota_total_jogo,
                    SUM(p.pontuacao_competidor_2) AS nota_total_competidor,
                    SUM(p.pontuacao_competidor_2 + p.pontuacao_jogo) AS nota_geral_competidor
                FROM
                    "Jogos" j
                JOIN
                    "Pontuacoes" p ON p.id_jogo = j.id
                GROUP BY
                    j.id, j.id_competidor_2
            ) AS notas_por_jogo
        ) AS p
        JOIN "Competidores" c ON c.id = p.id_competidor
        GROUP BY
            c.nome, p.id_competidor;
        """)

        result = await session.execute(query)
        rows = result.fetchall()

    for row in rows:
        notas_competidores.append({
            "nome_competidor": row[0],
            "id_competidor": str(row[1]),
            "total_jogo": row[2],
            "total_competidor": row[3],
            "nota_total": row[4]
        })

    content = {
        "message": "Notas de competidores",
        "response": notas_competidores
    }

    return JSONResponse(content=content)