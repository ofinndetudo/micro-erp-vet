from pydantic import BaseModel, Field
from typing import Optional, List

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
    quantidade_estoque: int

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True

# Esquemas para Vendas (Sprint 3)
class VendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)
    valor_total: float

# Esquemas para Financeiro (Sprint 3)
class FinanceiroBase(BaseModel):
    descricao: str
    valor: float
    tipo: str # 'RECEITA' ou 'DESPESA'
    plano_contas_id: int # Vínculo com a árvore de contas[cite: 1]

class Financeiro(FinanceiroBase):
    id: int

    class Config:
        from_attributes = True