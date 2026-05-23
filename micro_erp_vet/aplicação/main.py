from fastapi import FastAPI
from .database import engine, Base
from .routes import cadastros, vendas, financeiro

# Cria as tabelas no banco de dados se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Micro-ERP Veterinária")

# Inclui as rotas do sistema
app.include_router(cadastros.router)
app.include_router(compras.router)
app.include_router(vendas.router)
app.include_router(financeiro.router)
app.include_router(contabilidade.router)



@app.get("/")
def home():
    return {
        "status": "Sistema Online", 
        "projeto": "Micro-ERP Veterinária",
        "versao": "Final (Sprints 1-5)"  
    }