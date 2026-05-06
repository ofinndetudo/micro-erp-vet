from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])

@router.get("/fluxo-caixa/")
def obter_fluxo_caixa(db: Session = Depends(get_db)):
    # RF04: Demonstração de Entradas e Saídas
    receitas = db.query(models.Financeiro).filter(models.Financeiro.tipo == 'RECEITA').all()
    despesas = db.query(models.Financeiro).filter(models.Financeiro.tipo == 'DESPESA').all()
    
    # Vínculo com Plano de Contas
    total = sum(r.valor for r in receitas) - sum(d.valor for d in despesas)
    return {"saldo_atual": total, "historico": receitas + despesas}