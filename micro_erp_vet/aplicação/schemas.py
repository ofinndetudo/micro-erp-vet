from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Esquemas para Entidades (Clientes/Fornecedores)
class EntidadeBase(BaseModel):
    nome: str
    documento: str # CPF ou CNPJ
    tipo: str # 'CLIENTE' ou 'FORNECEDOR'

class EntidadeCreate(EntidadeBase):
    pass

class Entidade(EntidadeBase):
    id: int
    ativo: bool
    class Config:
        from_attributes = True

# Esquemas para Produtos
class ProdutoBase(BaseModel):
    nome: str
    sku: str # SKU único
    preco_custo: float = Field(gt=0)
    preco_venda: float = Field(gt=0)
    quantidade_estoque: int = Field(ge=0) #permite que o estoque chegue a zero
    estoque_minimo = int = 5

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    ativo: bool
    class Config:
        from_attributes = True

# Esquemas para Financeiro (Sprint 3)
class FinanceiroBase(BaseModel):
    descricao: str
    valor: float = Field(ge=0)
    tipo: str # 'RECEITA' ou 'DESPESA'
    status: str
    plano_contas_id: int # Vínculo com a árvore de contas[cite: 1]
    data_vencimento: Optional[datetime] = None

class Financeiro(FinanceiroBase):
    pass

class Financeiro(FinanceiroBase):
    id: int
    data_criacao: datetime
    class Config:
        from_attributes = True

# Esquemas para Vendas (Sprint 3)
class VendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)
    valor_total: float