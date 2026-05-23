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
        models.Financeiro.tipo == 'RECEITA',
        models.Financeiro.status == 'PAGO'
    ).scalar() or 0.0

    #busca o total de despesas de compras/operacional
    despesas = db.query(func.sum(models.Financeiro.valor)).filter(
        models.Financeiro.tipo  == 'DESPESA',
        models.Financeiro.status == 'PAGO'
    )scalar() or 0.0

    resultado = receitas - despesas
    
    return{
        "faturamento_bruto": receitas,
        "total_despesas": despesas,
        "lucro_prejuizo_liquido": resultado,
        "status":  "LUCRO" if resultado > 0 else "PREJUIZO"   
        }

@router.get("/balanco-patrimonial/")
def obter_balanco(db: Session = Depends(get_db)):
    #ativos (dinheiro no caixa e valor do estoque)
    caixa = db.query(func.sum(models.Financeiro)).filter(models.Financeiro.id_plano_contas == 1).scalar() or 0.0
    valor_estoque = db.query(func.sum(models.Financeiro.preco_custo * models.Produto.quantidade_estoque)).scalar() or 0.0


    return{
        "ativos"{
            "caixa_e_equivalentes": caixa,
            "estoque_total": valor_estoque,
            "total_ativos": valor_estoque
        },
        "passivos"{
            "contas_pagar": "Soma das obrigações pendentes"
        }
    }