from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from aplica_o.database import get_db
from aplica_o import models

# Define a rota que o FastAPI usará para buscar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verificar_usuario(login: str, senha_plana: str, db: Session):
    # RF03: Busca o usuário no banco de dados
    usuario = db.query(models.Usuario).filter(models.Usuario.login == login).first()
    if not usuario or not usuario.ativo:
        return None
    
    # Verificação simples de senha (em produção, usaria hash)
    if usuario.senha == senha_plana:
        return usuario
    return None

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Lógica para validar o token e retornar o usuário logado
    usuario = db.query(models.Usuario).filter(models.Usuario.login == token).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario

def verificar_permissao_adm(usuario: models.Usuario):
    if usuario.perfil != "ADMIN":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Acesso restrito a administradores."
        )
    return True  