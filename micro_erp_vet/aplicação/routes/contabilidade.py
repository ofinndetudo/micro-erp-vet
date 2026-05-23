from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from aplica_o.database import get_db
from aplica_o import models

router = APIRouter (prefix="/contabilidade", tags=["Contabilidade"])

@router.get("/dre/")
def calcular_dre (db: Session = Depends(get_db)):
    #busca o total das receitas de vendas
    receitas = db.query(func.sum(models.Financeiro.valor)).filter(
        models.Financeiro.tipo == 'Receber',
        models.Financeiro.status == 'Pago'
    ).scalar() or 0.0

    imposto = receitas * 0.10

    #busca o total de despesas de compras/operacional
    despesas = db.query(func.sum(models.Financeiro.valor)).filter(
        models.Financeiro.tipo  == 'Pagar',
        models.Financeiro.status == 'Pago'
    ).scalar() or 0.0

    resultado = receitas - despesas - impostos
    
    return{
        "faturamento_bruto": receitas,
        "impostos_simples_nacional": imposto,
        "total_despesas": despesas,
        "lucro_prejuizo_liquido": resultado,
        "status":  "LUCRO" if resultado > 0 else "PREJUIZO"   
        }

@router.get("/balanco-patrimonial/")
def obter_balanco(db: Session = Depends(get_db)):
    #ativos (dinheiro no caixa e valor do estoque)
    caixa = db.query(func.sum(models.Financeiro.valor)).filter(
        models.Financeiro.id_plano_contas == 1
        ).scalar() or 0.0
    valor_estoque = db.query(func.sum(models.Produto.preco_custo * models.Produto.quantidade_estoque)).scalar() or 0.0

    contas_pagar = db.query(func.sum(models.Financeiro.valor)).filter(
        models.Financeiro.tipo == 'Pagar',
        models.Financeiro.status == 'Pendente'
    ).scalar() or 0.0

    return{
        "ativos": {
            "caixa_e_equivalentes": caixa,
            "estoque_total": valor_estoque,
            "total_ativos": valor_estoque + caixa
        },
        "passivos": {
            "contas_pagar": contas_pagar,
            "total_passivos": contas_pagar
        }
    }