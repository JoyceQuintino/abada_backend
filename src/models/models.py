import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship, DeclarativeBase

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
    # competidor = relationship('Competidores', backref='Categorias')
    # graduacoes = relationship('Graduacoes', backref='Categorias')


class Graduacoes(Base):
    __tablename__ = 'Graduacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    id_categoria = Column('categoria_id', ForeignKey('Categorias.id', ondelete='CASCADE'))
    categoria = relationship("Categorias", foreign_keys=id_categoria)
    # categoria = relationship('Categorias', backref='Graduacoes')
    # competidor = relationship('Competidores', backref='Graduacoes')
    # filiacao = relationship('Filiacoes', backref='Graduacoes')


class Filiacoes(Base):
    __tablename__ = 'Filiacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    tipo = Column('tipo', String, nullable=False)
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id', ondelete='CASCADE'))
    graduacao = relationship("Graduacoes", foreign_keys=id_graduacao)
    # competidor = relationship('Competidores', backref='Filiacoes')


class Competidores(Base):
    __tablename__ = 'Competidores'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    apelido = Column('apelido', String, nullable=False)
    numero = Column('numero', Integer, nullable=True)
    # nota = Column('nota', Float, nullable=True)
    cidade = Column('cidade', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    idade = Column('idade', Integer, nullable=True)
    foto_url = Column('foto_url', String, nullable=True)
    id_filiacao = Column('id_filiacao', UUID(), ForeignKey('Filiacoes.id', ondelete='CASCADE'))
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id', ondelete='CASCADE'))
    filiacao = relationship("Filiacoes", foreign_keys=id_filiacao)
    graduacao = relationship("Graduacoes", foreign_keys=id_graduacao)


class Jogos(Base):
    __tablename__ = 'Jogos'
    id =  id_column()
    nota = Column('nota', Float, nullable=False)
    jogo_valido = Column('jogo_valido', Integer, nullable=False)
    id_competidor_1 = Column('id_competidor_1', UUID(), ForeignKey('Competidores.id', ondelete='CASCADE'))
    id_competidor_2 = Column('id_competidor_2', UUID(), ForeignKey('Competidores.id', ondelete='CASCADE'))
    id_modalidade = Column('id_modalidade', UUID(), ForeignKey('Modalidades.id', ondelete='CASCADE'))
    competidor_1 = relationship("Competidores", foreign_keys=[id_competidor_1])
    competidor_2 = relationship("Competidores", foreign_keys=[id_competidor_2])
    modalidade = relationship("Modalidades", foreign_keys=id_modalidade)


class Modalidades(Base):
    __tablename__ = 'Modalidades'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    # jogo = relationship('Jogos', backref='Modalidades')


class Pontuacoes(Base):
    __tablename__ = 'Pontuacoes'
    id =  id_column()
    pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
    pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
    pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
    id_jurado = Column('id_jurado', UUID(), ForeignKey('Jurados.id', ondelete='CASCADE'))
    id_jogo = Column('id_jogo', UUID(), ForeignKey('Jogos.id', ondelete='CASCADE'))
    jurado = relationship("Jurados", foreign_keys=id_jurado)
    jogo = relationship("Jogos", foreign_keys=id_jogo)


class Jurados(Base):
    __tablename__ = 'Jurados'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    # jurado = relationship('Pontuacoes', backref='Jurados')
    