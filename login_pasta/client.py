from sqlalchemy import create_engine, Column, String, Integer, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.schema import CreateSchema
from urllib.parse import quote

senha = "Lessypets987@"
senha_segura = quote(senha, safe="") 
 
DATABASE_URL = f"postgresql://postgres:{senha_segura}@db.xgokuxjnlcvyzpatobne.supabase.co:5432/postgres"

db = create_engine(DATABASE_URL)

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

def criar_schema(identificador):
    """Cria um schema no banco de dados com o nome do identificador"""
    identificador = identificador.replace(" ", "_").lower()
    
    with db.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{identificador}"'))
        conn.commit()
    return identificador

def criar_tabela(schema, nome_Pet):
    """Cria uma tabela dentro do schema"""
    class Pet(Base):
        __tablename__ = nome_Pet.replace(" ", "_").lower()
        __table_args__ = {"schema": schema}

        id = Column("id", Integer, primary_key=True, autoincrement=True)
        nome_pet = Column("nome_pet", String)
        idade = Column("idade", Integer)
        raca = Column("raca", String)

        def __init__(self, nome_pet, idade, raca):
            self.nome_pet = nome_pet
            self.idade = idade
            self.raca = raca

    Base.metadata.create_all(bind=db)
    return Pet

def cadastrar_dog(identificador, Nd, idade, Raca):
    """Registra um pet no banco"""
    schema = criar_schema(identificador) 
    Pet = criar_tabela(schema, Nd)

    novo_pet = Pet(nome_pet=Nd, idade=idade, raca=Raca)
    session.add(novo_pet)
    session.commit()
    session.close()
