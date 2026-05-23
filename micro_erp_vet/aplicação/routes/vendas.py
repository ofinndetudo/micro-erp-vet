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
    
    nova_venda = models.Venda(
        id_produto = venda.d-id_produto,
        quantidade = venda.quantidade,
        valor_total = venda.valor_total,
        data_venda = date.today()  
        )
    db.add(nova_venda)

    novo_recebivel = models.Financeiro(
        tipo = "RECEBER",
        valor = venda_data.valor_total,
        entidade_id = venda_data.cliente_id,
        data_vencimento = date.today(),
        status = "ABERTO",
        id_plano_contas = 115 #ID dos Clientes no plano de contas
    )

    db.add(novo_recebivel)

    try:
        db.commit()
        db.refresh(nova_venda)
        return {
            "status": "Venda realizada e estoque atualizado",
            "estoque_restante": produto.quantidade_estoque,
            "financeiro": "Título gerado no Contas a Receber"
            }

    except Exception as e:
        db.rollback()
        raise HTTPException (status_code = 500, detail = f"Erro ao processar venda: {str(e)}")    