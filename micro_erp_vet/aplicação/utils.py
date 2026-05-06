import re

# Função para validar formato básico de CPF ou CNPJ
def validar_documento(documento: str):
    # Remove caracteres não numéricos
    doc = re.sub(r'\D', '', documento)
    
    # Verifica se tem 11 dígitos (CPF) ou 14 dígitos (CNPJ)
    if len(doc) in [11, 14]:
        return True
    return False