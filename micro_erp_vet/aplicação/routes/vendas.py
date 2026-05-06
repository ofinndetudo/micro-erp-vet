from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.post("/registrar/")
def registrar_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == venda.produto_id).first()
    
    # Verificação de estoque antes da venda
    if not produto or produto.quantidade_estoque < venda.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente ou produto inativo")
    
    # RF03: Baixa automática de estoque
    produto.quantidade_estoque -= venda.quantidade
    
    nova_venda = models.Venda(**venda.dict())
    db.add(nova_venda)
    db.commit()
    return {"status": "Venda realizada e estoque atualizado"}