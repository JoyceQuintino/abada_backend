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

class Users(Base):
    __tablename__ = 'Users'
    id = id_column()
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)

class Categorias(Base):
    __tablename__ = 'Categorias'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)

class Graduacoes(Base):
    __tablename__ = 'Graduacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    id_categoria = Column('categoria_id', ForeignKey('Categorias.id', ondelete='CASCADE'))
    categoria = relationship("Categorias", foreign_keys=id_categoria)

class Filiacoes(Base):
    __tablename__ = 'Filiacoes'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)
    tipo = Column('tipo', String, nullable=False)
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id', ondelete='CASCADE'))
    graduacao = relationship("Graduacoes", foreign_keys=id_graduacao)

class Competidores(Base):
    __tablename__ = 'Competidores'
    id =  id_column()
    nome = Column('nome', String, nullable=False)
    apelido = Column('apelido', String, nullable=False, unique=True)
    numero = Column('numero', Integer, nullable=True)
    cidade = Column('cidade', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    idade = Column('idade', Integer, nullable=True)
    foto_url = Column('foto_url', String, nullable=True)
    id_filiacao = Column('id_filiacao', UUID(), ForeignKey('Filiacoes.id', ondelete='CASCADE'), nullable=True)
    id_graduacao = Column('id_graduacao', UUID(), ForeignKey('Graduacoes.id', ondelete='CASCADE'))
    filiacao = relationship("Filiacoes", foreign_keys=id_filiacao)
    graduacao = relationship("Graduacoes", foreign_keys=id_graduacao)

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "apelido": self.apelido,
            "numero": self.numero,
            "cidade": self.cidade,
            "estado": self.estado,
            "sexo": self.sexo,
            "idade": self.idade,
            "foto_url": self.foto_url,
            "id_filiacao": str(self.id_filiacao), 
            "id_graduacao": str(self.id_graduacao),  
        }

class Jogos(Base):
    __tablename__ = 'Jogos'
    id =  id_column()
    id_competidor_1 = Column('id_competidor_1', UUID(), ForeignKey('Competidores.id', ondelete='CASCADE'))
    id_competidor_2 = Column('id_competidor_2', UUID(), ForeignKey('Competidores.id', ondelete='CASCADE'))
    id_modalidade = Column('id_modalidade', UUID(), ForeignKey('Modalidades.id', ondelete='CASCADE'))
    id_categoria = Column('id_categoria', UUID(), ForeignKey('Categorias.id', ondelete='CASCADE'))
    fase = Column('fase', String, nullable=False)
    jogo_order = Column('jogo_order', Integer, nullable=False)
    competidor_1 = relationship("Competidores", foreign_keys=[id_competidor_1])
    competidor_2 = relationship("Competidores", foreign_keys=[id_competidor_2])
    modalidade = relationship("Modalidades", foreign_keys=id_modalidade)
    categoria = relationship("Categorias", foreign_keys=id_categoria)

    def to_dict(self):
        return {
            'id': str(self.id),
            'competidor_1': str(self.id_competidor_1),
            'competidor_2': str(self.id_competidor_2),
            'id_modalidade': str(self.id_modalidade),
            'modalidade': {  
                'id': str(self.modalidade.id),
                'nome': self.modalidade.nome
            },
            'id_categoria': str(self.id_categoria),
            'categoria': {
                'id': str(self.categoria.id),
                'nome': self.categoria.nome 
            },
            'fase': str(self.fase)
        }

class Modalidades(Base):
    __tablename__ = 'Modalidades'
    id =  id_column()
    nome = Column('nome', String, nullable=False, unique=True)

class Pontuacoes(Base):
    __tablename__ = 'Pontuacoes'
    id =  id_column()
    pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
    pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
    pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
    id_jogo = Column('id_jogo', UUID(), ForeignKey('Jogos.id', ondelete='CASCADE'))
    jogo_valido = Column('jogo_valido', Integer, nullable=False)
    id_user = Column('id_user', UUID(), ForeignKey('Users.id', ondelete='CASCADE'))
    jogo = relationship("Jogos", foreign_keys=id_jogo)
    user = relationship("Users", foreign_keys=id_user)

class Ranking(Base):
    __tablename__ = 'Ranking'
    id = id_column()
    apelido = Column('apelido', String, nullable=False)
    numero = Column('numero', Integer, nullable=False)
    sexo = Column('sexo', String, nullable=True)
    categoria = Column('categoria', String, nullable=False)
    fase = Column('fase', String, nullable=False)
    id_competidor = Column('id_competidor', UUID(), nullable=False)
    total_jogo = Column('total_jogo', Float, nullable=False)
    total_competidor = Column('total_competidor', Float, nullable=False)
    nota_total = Column('nota_total', Float, nullable=False)
