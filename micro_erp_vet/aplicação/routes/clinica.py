# Dados fixos da Clínica (Configurações do Sistema)

CLINICA_DADOS = {
    "nome_fantasia": "Pet Care Maio 2026",
    "razao_social": "Fulano de town Veterinaria LTDA",
    "cnpj": "12.345.678/0001-90",
    "endereco": "Rua da Tecnologia, 101 - Hub TI",
    "cidade": "Uberlândia - MG",
    "telefone": "(34) 99999-0000",
    "responsavel_tecnico": "Dr. Fulano",
    "regime_tributario": "Simples Nacional (10%)"
}

def obter_cabecalho_relatorio():
    return f"{CLINICA_DADOS['nome_fantasia']} - CNPJ: {CLINICA_DADOS['cnpj']}"