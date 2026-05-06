from sqlalchemy.orm import Session
from .models import Produto, EstoqueLog, PedidoCompra, ItemCompra
import datetime

# Função que executa a lógica de recebimento de mercadorias (RF07 e RF09)
def processar_recebimento_compra(db: Session, pedido_id: int):
    # Localiza o pedido de compra no banco de dados
    pedido = db.query(PedidoCompra).filter(PedidoCompra.id == pedido_id).first()
    
    # Verifica se o pedido existe e se ainda não foi recebido para evitar duplicidade
    if not pedido or pedido.status == "Recebido":
        return None

    # Percorre cada item que consta no pedido de compra
    for item in pedido.itens:
        produto = db.query(Produto).filter(Produto.id == item.id_produto).first()
        
        if produto:
            # Cálculo do Custo Médio Ponderado exigido na Sprint 2
            valor_estoque_antigo = produto.estoque_atual * produto.preco_custo
            valor_novo_lote = item.quantidade * item.preco_unitario
            novo_saldo_total = produto.estoque_atual + item.quantidade
            
            novo_custo_medio = (valor_estoque_antigo + valor_novo_lote) / novo_saldo_total
            
            # Atualiza os valores no cadastro do produto
            produto.preco_custo = novo_custo_medio
            produto.estoque_atual = novo_saldo_total
            
            # Registra o histórico da movimentação para auditoria (RF11)
            log = EstoqueLog(
                id_produto=produto.id,
                quantidade_alterada=item.quantidade,
                tipo_movimentacao="Entrada",
                motivo=f"Recebimento Pedido Compra #{pedido.id}",
                data=datetime.datetime.utcnow()
            )
            db.add(log)

    # Altera o status do pedido para que ele não possa ser processado novamente
    pedido.status = "Recebido"
    
    # Salva todas as alterações de uma vez no banco de dados
    db.commit()
    db.refresh(pedido)
    return pedido

# Função para verificar se o estoque está baixo (RF10)
def verificar_alerta_estoque(db: Session, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    # Retorna verdadeiro se o estoque atual for menor ou igual ao mínimo definido
    if produto and produto.estoque_atual <= produto.estoque_minimo:
        return True
    return False

# Função para processar a entrada de mercadoria conforme RF09
def atualizar_estoque_e_custo(db, id_produto, qtd_nova, preco_compra):
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    
    # Cálculo do Custo Médio exigido na Sprint 2
    valor_total_atual = produto.estoque_atual * produto.preco_custo
    valor_novo_lote = qtd_nova * preco_compra
    novo_saldo = produto.estoque_atual + qtd_nova
    
    # Nova média ponderada
    novo_custo_medio = (valor_total_atual + valor_novo_lote) / novo_saldo
    
    # Atualização dos dados no banco
    produto.preco_custo = novo_custo_medio
    produto.estoque_atual = novo_saldo
    
    return produto

# Rota que o sistema usa para confirmar o recebimento (RF07)
@router.post("/confirmar-recebimento/{pedido_id}")
def confirmar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    # 1. Busca os itens do pedido
    # 2. Para cada item, chama a função do services.py
    # 3. Gera o rastro (log) de movimentação (RF11)
    pass