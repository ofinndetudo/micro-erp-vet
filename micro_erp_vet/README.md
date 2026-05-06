══════════════════════════════════════════════════════════════
                    Micro-ERP Veterinária
══════════════════════════════════════════════════════════════

Sistema de gestão para clínicas veterinárias focado em controle de cadastros, movimentação de estoque, fluxo de caixa e geração de relatórios técnicos. Este projeto foi desenvolvido como parte dos requisitos das Sprints 1, 2 e 3 do curso.

══════════════════════════════════════════════════════════════
                        Estrutura do Projeto
══════════════════════════════════════════════════════════════

O sistema utiliza uma arquitetura modular para garantir a escalabilidade e organização do código:

├── aplica_o/routes/
│   └── Contém os endpoints divididos por domínios (cadastros, vendas, financeiro, clinica).
│
├── aplica_o/models.py
│   └── Definição das tabelas do banco de dados (Entidades, Produtos, Usuarios, Financeiro).
│
├── aplica_o/schemas.py
│   └── Validação de dados de entrada e saída via Pydantic.
│
├── aplica_o/utils.py
│   └── Funções utilitárias, incluindo o validador de CPF/CNPJ (Requisito RF01).
│
├── aplica_o/reports/
│   └── Módulo responsável pela geração de relatórios em formato PDF.
│
└── aplica_o/auth.py
    └── Sistema de autenticação e proteção de rotas.

══════════════════════════════════════════════════════════════
                     Requisitos Implementados
══════════════════════════════════════════════════════════════

▸ Sprint 1: O Alicerce  
   ────────────────────────────────
   • Configuração do ambiente com FastAPI e SQLAlchemy.  
   • Criação da estrutura de pastas e banco de dados relacional.  
   • Modelagem do Plano de Contas conforme especificações contábeis.  

▸ Sprint 2: Regras de Negócio  
   ────────────────────────────────
   • Validação obrigatória de documentos (CPF/CNPJ) no cadastro de clientes e fornecedores.  
   • Implementação do controle de estoque com baixa automática após vendas (RF03).  
   • Lógica de desabilitação de registros (soft delete) utilizando o campo 'ativo'.  

▸ Sprint 3: Financeiro e Saídas  
   ────────────────────────────────
   • Registro de movimentações financeiras vinculadas ao Plano de Contas (RF04).  
   • Geração de relatórios gerenciais em PDF para controle de estoque e vendas.  
   • Interface de documentação automática via Swagger.  

══════════════════════════════════════════════════════════════
                  Como Executar o Projeto
══════════════════════════════════════════════════════════════

Certifique-se de ter o Python instalado em sua máquina.

Instale as dependências necessárias:

Bash
────────────────────────────
pip install -r requirements.txt

Inicie o servidor de desenvolvimento:

Bash
────────────────────────────
uvicorn aplica_o.main:app --reload

Acesse a documentação interativa para testar as rotas:

http://127.0.0.1:8000/docs

══════════════════════════════════════════════════════════════
                   Tecnologias Utilizadas
══════════════════════════════════════════════════════════════

• FastAPI  
• SQLAlchemy  
• Pydantic  
• SQLite  
• FPDF (Geração de relatórios)