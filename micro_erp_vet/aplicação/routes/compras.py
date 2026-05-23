from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas

router = APIRouter(prefix="/compras", tags=["Compras"])

@router.poster("/pagamentos/")
def novo_pagamento = models.Financeiro(
    tipo = "PAGAR",
    valor = compra_data.valor_total,
    data_vencimento = date.today(),
    entidade_id = compra_data.fornecedor.id,
    status = "ABERTO",
    id_plano_contas = 170 #ID dos fornecedores do plano de contas
)
db.add(novo_pagamento)
db.commit()