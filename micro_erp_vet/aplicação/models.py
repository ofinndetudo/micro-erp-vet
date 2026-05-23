from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

#tabela de usuários para o sistema de login (RF03)
class Usuario(base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    login = Column(String, unique=True)
    senha = Column(String) # No mundo real, usaríamos hash
    perfil = Column(String) # Admin ou Vendedor
    ativo = Column(Boolean, default=True)

# Cadastro de Clientes e Fornecedores conforme Requisito RF01
class Entidade(Base):
    __tablename__ = "entidades"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    documento = Column(String, unique=True) # CPF ou CNPJ validado
    tipo = Column(String) # 'Cliente' ou 'Fornecedor'
    pets = relationship("Pet", back_populates="dono")

# Entidade Pet do seu diagrama original
class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    especie = Column(String)
    raca = Column(String)
    idade = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("entidades.id"))
    dono = relationship("Entidade", back_populates="pets")

# Módulo de Produtos com SKU e Estoque Mínimo (RF02)
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sku = Column(String, unique=True) # Código único exigido no trabalho
    preco_custo = Column(Float)
    preco_venda = Column(Float)
    estoque_atual = Column(Integer)
    estoque_minimo = Column(Integer) # Usado para alertas de reposição
    ativo = Column(Boolean, default=True)

# Plano de Contas Hierárquico exigido para Contabilidade (RF04/Anexo 1)
class PlanoContas(Base):
    __tablename__ = "plano_contas"
    id = Column(Integer, primary_key=True)
    codigo = Column(String, unique=True) # Ex: 1.1.1.1 (Caixa)
    nome = Column(String)
    tipo = Column(String) # Ativo, Passivo, Patrimônio, Receita ou Despesa

# Gestão Financeira integrada com Vendas e Compras (RF17/RF18)
class Financeiro(Base):
    __tablename__ = "financeiro"
    id = Column(Integer, primary_key=True)
    tipo = Column(String) # 'Receber' ou 'Pagar'
    valor = Column(Float)
    status = Column(String, default="Pendente") # Pago ou Pendente
    data_vencimento = Column(DateTime)
    # Vinculo com o Plano de Contas para o Balanço Patrimonial futuro
    id_plano_contas = Column(Integer, ForeignKey("plano_contas.id"))
    entidade_id = Column(Integer, ForeignKey("entidades.id"))

# Tabela para registrar o Pedido de Compra (RF06)
class PedidoCompra(Base):
    __tablename__ = "pedidos_compra"
    id = Column(Integer, primary_key=True)
    id_fornecedor = Column(Integer, ForeignKey("entidades.id"))
    data_pedido = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String) # Ex: 'Pendente', 'Recebido'
    itens = relationship("ItemCompra", back_populates="pedido")

# Itens específicos do pedido (RF06)
class ItemCompra(Base):
    __tablename__ = "itens_compra"
    id = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey("pedidos_compra.id"))
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    pedido = relationship("PedidoCompra", back_populates="itens")

# Rastro de Auditoria: Log de Movimentações (RF11)
class EstoqueLog(Base):
    __tablename__ = "estoque_log"
    id = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    quantidade_alterada = Column(Integer)
    tipo_movimentacao = Column(String) # 'Entrada (Compra)' ou 'Saida (Venda)'
    data = Column(DateTime, default=datetime.datetime.utcnow)
    motivo = Column(String) # Ex: Recebimento de Pedido #123    