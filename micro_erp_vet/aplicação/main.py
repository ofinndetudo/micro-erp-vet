from fastapi import FastAPI
from .database import engine, Base
from .routes import cadastros # Vamos criar este a seguir

# Cria as tabelas no banco de dados se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Micro-ERP Veterinária")

# Inclui as rotas do sistema
app.include_router(cadastros.router)

@app.get("/")
def home():
    return {"status": "Sistema Online", "sprint": 1}