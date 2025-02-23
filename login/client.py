from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import main

db = create_engine(f"sqlite:///login/clients/{main.identificador}.db")
Session = sessionmaker(bind=db)
session = Session()

Client = declarative_base()

class client(Client):
    __tablename__ = main.identificador

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_pet = Column("nome_pet", String)
    idade = Column("idade", Integer)
    raca = Column("raca", String)

    def __init__(self, nome_pet, idade, raca):
        self.nome_pet = nome_pet
        self.idade = idade
        self.raca = raca


Client.metadata.create_all(bind=db)

def cadastrar_dog(Nd, idade, Raca):
    dog = client(nome_pet=Nd, idade=idade, raca=Raca)
    session.add(dog)
    session.commit()
