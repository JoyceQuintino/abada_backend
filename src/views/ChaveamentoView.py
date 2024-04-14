from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from src.services.ChaveamentoService import ChaveamentoService
from src.schemas import ChaveamentoSchema
from src.database.db_connection import async_session
from src.schemas.ChaveamentoSchema import ChaveamentoInput, CategoriaInput
from sqlalchemy import text

tokens_validos = ['08f57f2c-ac47-4e52-8098-f3fce671b0f0']

chaveamento_router = APIRouter(prefix='/chaveamento', tags=['Chaveamento'])
assets_router = APIRouter(prefix='/assets')

@chaveamento_router.post('/categoria_teste')
async def chaveamento_jogos_teste(payload: ChaveamentoInput, request: Request):
    return await ChaveamentoService.chaveamento_categoria_teste(categoria=payload.model_dump()['categoria'])

@chaveamento_router.get('/get_all_chaveamento', summary="Obter todos os jogadores")
async def get_all_chaveamento(request: Request):
    """
    Obtém todos os jogadores.

    Returns:
        List[dict]: Lista de dicionários contendo os dados dos jogadores.
    """
    return await ChaveamentoService().get_all_chaveamento()

@chaveamento_router.post('/categoria', summary="Gerar chaveamento de jogos para uma categoria")
async def chaveamento_jogos(payload: ChaveamentoInput, request: Request):
    """
    Gera chaveamento de jogos para uma categoria.

    Args:
        payload (ChaveamentoInput): Objeto contendo os dados da categoria.

    Returns:
        dict: Dicionário contendo o chaveamento da categoria.
    """

    if payload.token not in tokens_validos:
        raise HTTPException(status_code=403, detail="Token inválido")

    if payload.categorias:
        return await ChaveamentoService().chaveamento_categoria(payload.categorias)
    else:
        raise HTTPException(status_code=400, detail="Nenhuma categoria fornecida no payload")

@chaveamento_router.get('/get_jogos/{fase}', response_model=ChaveamentoSchema.StandardOutput, responses={400: {'model': ChaveamentoSchema.ErrorOutput}})
async def get_all_players_by_step(fase: str):
    jogos = []

    try:
        async with async_session() as session:
            query = text(""" 
                SELECT 
                    j.id AS jogo_id,
                    Competidores1.apelido AS competidor_1,
	                Competidores1.numero AS numero_competidor_1,
                    Competidores2.apelido AS competidor_2,
	                Competidores2.numero AS numero_competidor_2,
                    m.nome AS modalidade_nome,
	                c.nome AS categoria_nome,
                    j.fase AS fase
                FROM 
                    "Jogos" j
                LEFT JOIN 
                    "Competidores" AS Competidores1 ON j.id_competidor_1 = Competidores1.id
                LEFT JOIN 
                    "Competidores" AS Competidores2 ON j.id_competidor_2 = Competidores2.id
                JOIN 
                    "Modalidades" m ON j.id_modalidade = m.id
                JOIN
	                "Categorias" c ON j.id_categoria = c.id
                WHERE j.fase = :fase;
            """)

            result = await session.execute(query, {"fase": fase})
            jogos_by_fase = result.fetchall()

        for row in jogos_by_fase:
            jogos.append({
                "id_jogo": str(row[0]),
                "apelido_competidor_1": row[1],
                "numero_competidor_1": row[2],
                "apelido_competidor_2": row[3],
                "numero_competidor_2": row[4],
                "modalidade_nome": row[5],
                "categoria_nome": row[6],
                "fase": row[7]
            })

        content = {
            "jogos": jogos
        }

    finally:
        await session.close()

    return JSONResponse(content=content)
