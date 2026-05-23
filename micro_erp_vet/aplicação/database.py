from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Define o local do arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./clinica_erp.db"

# Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Configura a sessão de uso do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que as tabelas vão herdar
class Base(DeclarativeBase):
    pass

# Função auxiliar para obter a conexão nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()