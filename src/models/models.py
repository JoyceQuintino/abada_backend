import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CategoriaEnum(enum.Enum):
    laranja_laranja_azul = 'laranja_laranja_azul'
    azul_azul_verde = 'azul_azul_verde'
    verde_verde_roxa = 'verde_verde_roxa'
    roxa_roxa_marrom = 'roxa_roxa_marrom'
    marrom_marrom_vermelha = 'marrom_marrom_vermelha'
    Baoba = 'baoba'
class Filiacao(Base):
    __tablename__ = 'Filiacao'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome_professor = Column('nome_professor', String, nullable=False)
    graduacao_professor = Column('graduacao_professor', String, nullable=False)
    competidor = relationship('Competidor', backref='Filiacao')
class Graduacao(Base):
    __tablename__ = 'Graduacao'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    categoria = Column('categoria', Enum(CategoriaEnum), nullable=False)
    competidor = relationship('Competidor', backref='Graduacao')
class Competidor(Base):
    __tablename__ = 'Competidor'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=True)
    apelido = Column('apelido', String, nullable=False)
    nome_estado = Column('nome_estado', String, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    idade = Column('idade', Integer, nullable=True)
    id_filiacao = Column('id_filiacao', Integer, ForeignKey('Filiacao.id'))
    id_graduacao = Column('id_graduacao', Integer, ForeignKey('Graduacao.id'))
class Jogo(Base):
    __tablename__ = 'Jogo'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nota = Column('nota', Float, nullable=False)
    jogo_valido = Column('jogo_valido', Integer, nullable=True)
    id_competidor_1 = Column('id_competidor_1', Integer, ForeignKey('Competidor.id'))
    id_competidor_2 = Column('id_competidor_2', Integer, ForeignKey('Competidor.id'))
    id_modalidade = Column('id_modalidade', Integer, ForeignKey('Modalidade.id'))
    id_pontuacao = Column('id_pontuacao', Integer, ForeignKey('Pontuacao.id'))
class Modalidade(Base):
    __tablename__ = 'Modalidade'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    jogos = relationship('Jogo', backref='Modalidade')
class Pontuacao(Base):
    __tablename__ = 'Pontuacao'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
    pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
    pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
    id_jurado = Column('id_jurado', Integer, ForeignKey('Jurado.id'))
    id_jogo = Column('id_jogo', Integer, ForeignKey('Jogo.id'))
class Jurado(Base):
    __tablename__ = 'Jurado'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)

    