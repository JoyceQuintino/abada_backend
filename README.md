# Abadá Capoeira - API para Jogos Competitivos

Esta é a API da aplicação web para os jogos competitivos da Abadá-Capoeira Ceará, desenvolvida em Python utilizando frameworks como FastAPI e SQLAlchemy.

## Requisitos do Sistema

- [Python](https://www.python.org/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [pgAdmin](https://www.pgadmin.org/)

## Configuração do Ambiente

### Windows/Linux/MacOS

1. Certifique-se de ter, no mínimo, Python 3.11 instalado em seu sistema.
2. Certifique-se de estar no ambiente python com o pipenv e instalar as dependências:

    `pipenv shell && pipenv install`   
3. Certifique-se de possuir uma versão estável do Docker instalado em sua máquina.
4. Após isso, certifique-se de possuir o arquivo `.env` com as credenciais para subir o container com o banco de dados PostgreSQL.
5. Certifica-se do arquivo `.yml` existir e suba o container com o seguinte comando:
   
   `docker-compose up -d`
6. Após o container estar funcionando, execute o arquivo `init_db.py`, presente no caminho `src/database`.
7. Com isso, já possui o básico para fazer o sistema funcionar, bastando utilizar o seguinte comando para rodar a API:
   
   `uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8080`

8. A aplicação estará disponível em `http://localhost:8000`.

9. Para executar as migrations, primeiramente precisa gerar um script que lista as alterações realizadas com o seguinte comando: 
   `alembic revision --autogenerate -m'comments about update'`

   e depois para aplicar precisa utilizar o seguinte comando:
   `alembic upgrade head`

## Estrutura do Projeto

- `src/`: Diretório principal do projeto, contendo todos os demais diretórios do projeto.
- `src/api/main.py`: Arquivo principal que contém a configuração da aplicação FastAPI.
- `src/models`: Definição dos modelos de dados utilizando SQLAlchemy.
- `src/schemas`: Definição dos esquemas utilizados nos modelos da aplicação.
- `src/utils`: Funcões auxiliares.
- `src/services`: Controladores da aplicação.
- `src/views`: Rotas da aplicação.
- `src/database/init_db.py`: Configuração e inicialização da conexão com o banco de dados.
- `src/tests`: Testes unitários da aplicação.
- `.env`: Arquivo contendo as credenciais para o banco de dados.
- `migrations`: Definição das versões atualizadas dos models

## Licença

Este projeto é distribuído sob a [Licença MIT](LICENSE).