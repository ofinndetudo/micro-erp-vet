from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])

@router.get("/fluxo-caixa/")
def obter_fluxo_caixa(db: Session = Depends(get_db)):
    # RF04: Demonstração de Entradas e Saídas
    receitas = db.query(models.Financeiro).filter(models.Financeiro.tipo == 'Receber').all()
    despesas = db.query(models.Financeiro).filter(models.Financeiro.tipo == 'Pagar').all()
    
    # Vínculo com Plano de Contas
    total_receber = sum(r.valor for r in receitas) 
    total_pagar = sum(d.valor for d in despesas)
    saldo = total_receber - total_pagar

    return {
        "saldo_projetado": saldo, 
        "total_receber": total_receber,
        "total_pagar": total_pagar,
        "detalhes": {
            "entradas": receitas,
            "saidas": despesas
        }
    }