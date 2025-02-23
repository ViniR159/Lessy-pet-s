from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///login/clients/test.db")
Session = sessionmaker(bind=db)
session = Session()

Client = declarative_base()

class client(Client):
    __tablename__ = "Client"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_pet = Column("nome_pet", String)
    idade = Column("idade", Integer)
    especie = Column("especie", Integer)
    raca = Column("raca", String)

    def __init__(self, nome_pet, idade, especie, raca):
        self.nome_pet = nome_pet
        self.idade = idade
        self.especie = especie
        self.raca = raca


Client.metadata.create_all(bind=db)

def cadastrar_dogn(Nd, idade, especie, Raca):
    pessoa = client(nome_pet=Nd, idade=idade, especie=especie, raca=Raca)
    session.add(pessoa)
    session.commit()
