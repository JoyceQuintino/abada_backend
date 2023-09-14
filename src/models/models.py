import enum

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

class Categorias(Base):
    __tablename__ = 'Categorias'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    competidor = relationship('Graduacoes', backref='Categorias')
class Filiacoes(Base):
    __tablename__ = 'Filiacoes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    graduacao = Column('graduacao', String, nullable=False)
    tipo = Column('tipo', String, nullable=False)
    competidor = relationship('Competidores', backref='Filiacoes')
class Graduacoes(Base):
    __tablename__ = 'Graduacoes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    categoria = relationship('Categorias', backref='Graduacoes')
    competidor = relationship('Competidores', backref='Graduacoes')
class Competidores(Base):
    __tablename__ = 'Competidores'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    apelido = Column('apelido', String, nullable=False)
    numero = Column('numero', Integer, nullable=False)
    cidade = Column('cidade', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    idade = Column('idade', Integer, nullable=True)
    id_filiacao = Column('id_filiacao', Integer, ForeignKey('Filiacoes.id'))
    id_graduacao = Column('id_graduacao', Integer, ForeignKey('Graduacoes.id'))
    jogo_competidor_1 = relationship('Jogos', backref='Competidores')
    jogo_competidor_2 = relationship('Jogos', backref='Competidores')
class Jogos(Base):
    __tablename__ = 'Jogos'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nota = Column('nota', Float, nullable=False)
    jogo_valido = Column('jogo_valido', Integer, nullable=False)
    id_competidor_1 = Column('id_competidor_1', Integer, ForeignKey('Competidores.id'))
    id_competidor_2 = Column('id_competidor_2', Integer, ForeignKey('Competidores.id'))
    id_modalidade = Column('id_modalidade', Integer, ForeignKey('Modalidades.id'))
    id_pontuacao = Column('id_pontuacao', Integer, ForeignKey('Pontuacoes.id'))
class Modalidades(Base):
    __tablename__ = 'Modalidades'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    jogo = relationship('Jogos', backref='Modalidades')
class Pontuacoes(Base):
    __tablename__ = 'Pontuacoes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
    pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
    pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
    id_jurado = Column('id_jurado', Integer, ForeignKey('Jurados.id'))
    id_jogo = Column('id_jogo', Integer, ForeignKey('Jogos.id'))
class Jurados(Base):
    __tablename__ = 'Jurados'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    jurado = relationship('Pontuacoes', backref='Jurados')
    