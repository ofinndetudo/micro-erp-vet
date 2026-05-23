import re

# Função para validar formato básico de CPF ou CNPJ
def validar_documento(documento: str) -> bool:

    if not documento:
        return false
    # Remove caracteres não numéricos
    doc = re.sub(r'\D', '', documento)
    
    # Verifica se tem 11 dígitos (CPF) ou 14 dígitos (CNPJ)
    if len(doc) > 0 and doc == doc [0] * len(doc):
        return False

    #tamanho padrão de documentação
    return len(doc) in [11,14]

def limpar_documento(documento: str) -> str:
    return re.sub(r'\D',  '', documento)

def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:.2f}".replace(',', 'X').replace('.',',').replace('X','.')