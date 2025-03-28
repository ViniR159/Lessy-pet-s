from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text
from urllib.parse import quote

senha = "Lessypets987@"
senha_segura = quote(senha, safe="") 
 
DATABASE_URL = f"postgresql://postgres:{senha_segura}@db.xgokuxjnlcvyzpatobne.supabase.co:5432/postgres"

db = create_engine(DATABASE_URL)

Session = sessionmaker(bind=db)
session = Session()

Login = declarative_base()

class login(Login):
    __tablename__ = "login"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    quant_dogs = Column("quant_dogs", Integer)

    def __init__(self, nome, email, senha, quant_dogs):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.quant_dogs = quant_dogs

Login.metadata.create_all(bind=db)

def criar(Nome, Email, Senha, Quant):
    pessoa = login(nome=Nome, email=Email, senha=Senha, quant_dogs=Quant)
    session.add(pessoa)
    session.commit()