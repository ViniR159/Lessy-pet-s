from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Client = declarative_base()
def criar_arquivo(identificador):
    
    identificador = identificador
    caminho_db = f"login_pasta/clients/{identificador}.db"

    pasta= f"{identificador}/"
    if(not os.path.exists(pasta)):
        os.mkdir(pasta)
    else:
        print("hummm")
    print("print")
    
    
    os.makedirs(os.path.dirname(caminho_db), exist_ok=True)

    db = create_engine(f"sqlite:///{caminho_db}")
    Session = sessionmaker(bind=db)
    session = Session()

    return db, session

class client(Client):
    __tablename__ = "pet"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_pet = Column("nome_pet", String)
    idade = Column("idade", Integer)
    raca = Column("raca", String)

    def __init__(self, nome_pet, idade, raca):
        self.nome_pet = nome_pet
        self.idade = idade
        self.raca = raca

def cadastrar_dog(identificador, Nd, idade, Raca):
    engine, session = criar_arquivo(identificador)

    Client.metadata.create_all(bind=engine)

    dog = client(nome_pet=Nd, idade=idade, raca=Raca)
    session.add(dog)
    session.commit()
    session.close()
