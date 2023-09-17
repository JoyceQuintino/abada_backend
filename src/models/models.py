import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

"""
laranja_laranja_azul = 'laranja_laranja_azul'
    azul_azul_verde = 'azul_azul_verde'
    verde_verde_roxa = 'verde_verde_roxa'
    roxa_roxa_marrom = 'roxa_roxa_marrom'
    marrom_marrom_vermelha = 'marrom_marrom_vermelha'
    Baoba = 'baoba'
"""

ID_COLUMN_NAME = "id"

def id_column():
    import uuid
    return Column(ID_COLUMN_NAME,UUID(),primary_key=True,default=uuid.uuid4)

class Categorias(Base):
    __tablename__ = 'Categorias'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    competidor = relationship('Graduacoes', backref='Categorias')
class Graduacoes(Base):
    __tablename__ = 'Graduacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    categoria = relationship('Categorias', backref='Graduacoes')
    competidor = relationship('Competidores', backref='Graduacoes')
    filiacao = relationship('Filiacoes', backref='Graduacoes')
class Filiacoes(Base):
    __tablename__ = 'Filiacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    tipo = Column('tipo', String, nullable=False)
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id'))
    competidor = relationship('Competidores', backref='Filiacoes')
class Competidores(Base):
    __tablename__ = 'Competidores'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    apelido = Column('apelido', String, nullable=False)
    numero = Column('numero', Integer, nullable=True)
    cidade = Column('cidade', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    idade = Column('idade', Integer, nullable=True)
    foto_url = Column('foto_url', String, nullable=True)
    id_filiacao = Column('id_filiacao', UUID(), ForeignKey('Filiacoes.id'))
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id'))
    jogo_competidor_1 = relationship('Jogos', backref='Competidores')
    jogo_competidor_2 = relationship('Jogos', backref='Competidores')
class Jogos(Base):
    __tablename__ = 'Jogos'
    id =  id_column()
    nota = Column('nota', Float, nullable=False)
    jogo_valido = Column('jogo_valido', Integer, nullable=False)
    id_competidor_1 = Column('id_competidor_1', UUID(), ForeignKey('Competidores.id'))
    id_competidor_2 = Column('id_competidor_2', UUID(), ForeignKey('Competidores.id'))
    id_modalidade = Column('id_modalidade', UUID(), ForeignKey('Modalidades.id'))
    id_pontuacao = Column('id_pontuacao', UUID(), ForeignKey('Pontuacoes.id'))
class Modalidades(Base):
    __tablename__ = 'Modalidades'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    jogo = relationship('Jogos', backref='Modalidades')
class Pontuacoes(Base):
    __tablename__ = 'Pontuacoes'
    id =  id_column()
    pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
    pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
    pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
    id_jurado = Column('id_jurado', UUID(), ForeignKey('Jurados.id'))
    id_jogo = Column('id_jogo', UUID(), ForeignKey('Jogos.id'))
class Jurados(Base):
    __tablename__ = 'Jurados'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    jurado = relationship('Pontuacoes', backref='Jurados')
    