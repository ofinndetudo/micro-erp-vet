from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models, schemas, utils

router = APIRouter(prefix="/cadastros", tags=["Cadastros"])

@router.post("/entidade/", response_model=schemas.Entidade)
def criar_entidade(entidade: schemas.EntidadeCreate, db: Session = Depends(get_db)):
    # RF01: Validação de CPF/CNPJ obrigatória
    if not utils.validar_documento(entidade.documento):
        raise HTTPException(status_code=400, detail="Documento CPF/CNPJ inválido")
    
    nova_entidade = models.Entidade(**entidade.dict(), ativo=True)
    db.add(nova_entidade)
    db.commit()
    db.refresh(nova_entidade)
    return nova_entidade

@router.delete("/entidade/{entidade_id}")
def desabilitar_entidade(entidade_id: int, db: Session = Depends(get_db)):
    # Regra: Não excluir, apenas desabilitar
    entidade = db.query(models.Entidade).filter(models.Entidade.id == entidade_id).first()
    if not entidade:
        raise HTTPException(status_code=404, detail="Entidade não encontrada")
    entidade.ativo = False
    db.commit()
    return {"message": "Entidade desabilitada com sucesso"}