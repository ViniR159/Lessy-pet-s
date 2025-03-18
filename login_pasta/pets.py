from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Pet = declarative_base()
def criar_arquivo(identificador, nome_pet):
  
    caminho_db = f"login_pasta/clients/{identificador}/{nome_pet}.db"    
    
    os.makedirs(os.path.dirname(caminho_db), exist_ok=True)

    db = create_engine(f"sqlite:///{caminho_db}")
    Session = sessionmaker(bind=db)
    session = Session()

    return db, session

class pet(Pet):
    __tablename__ = "pet"

    Visita = Column("id", Integer, primary_key=True, autoincrement=True)
    pacote = Column("pacote", String)
    data_agendamento = Column("data do agendamento", String)
    Valor = Column("valor", String)

    def __init__(self, Valor, data_agendamento, pacote):
        self.Valor = Valor
        data_agendamento = data_agendamento
        self.pacote = pacote

def criar_arquivo_pet(identificador, nome_pet, Valor, data, pacote):
    engine, session = criar_arquivo(identificador, nome_pet)

    pet.metadata.create_all(bind=engine)

    dog = pet(pacote=pacote, data_agendamento=data, Valor=Valor)
    session.add(dog)
    session.commit()
    session.close()
