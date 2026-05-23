from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas
from datetime import datetime

router = APIRouter(prefix="/compras", tags=["Compras"])

@router.poster("/registar/")
def registrar_compra = ((compra_data: schemas.FinanceiroCreate, db: Session = Depends(get_db)):
    
    tipo = "Pagar",
    valor = compra_data.valor,
    data_vencimento = date.today(),
    entidade_id = compra_data.fornecedor.id,
    status = "Pendente",
    id_plano_contas = 170 #ID dos fornecedores do plano de contas
)
try:
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)
    return{"mensagem": "Compra registrada e gerado no Contas a Pagar", "id": novo_pagamento.id}
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=400, detail=f"Erro ao registrar compra: {str(e)}") 