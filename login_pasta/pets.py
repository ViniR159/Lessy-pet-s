from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote

senha = "Lessypets987@"
senha_segura = quote(senha, safe="") 
 
DATABASE_URL = f"postgresql://postgres:{senha_segura}@db.xgokuxjnlcvyzpatobne.supabase.co:5432/postgres"

db = create_engine(DATABASE_URL)

Session = sessionmaker(bind=db)
session = Session()

# Base para os modelos
Base = declarative_base()

def criar_tabela(schema, nome_pet):
    """Cria a tabela 'nome_pet_informacoes' dentro do schema"""
    nome_tabela = f"{nome_pet.replace(' ', '_').lower()}_visitas"

    class PetInfo(Base):
        __tablename__ = nome_tabela
        __table_args__ = {"schema": schema}

        id = Column("id", Integer, primary_key=True, autoincrement=True)
        pacote = Column("pacote", String)
        data_agendamento = Column("data_do_agendamento", String)
        valor = Column("valor", String)

        def __init__(self, pacote, data_agendamento, valor):
            self.pacote = pacote
            self.data_agendamento = data_agendamento
            self.valor = valor

    Base.metadata.create_all(bind=db)
    return PetInfo

def cadastrar_informacoes(identificador, nome_pet, valor, data, pacote):
    """Registra informações do pet no banco"""
    PetInfo = criar_tabela(identificador, nome_pet)

    nova_visita = PetInfo(pacote=pacote, data_agendamento=data, valor=valor)
    session.add(nova_visita)
    session.commit()
    session.close()
