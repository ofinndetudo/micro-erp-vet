from fpdf import FPDF
from aplica_o.models import Produto
from datetime import datetime

def gerar_relatorio_estoque(produtos: list[Produto]):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Relatório de Estoque - Micro-ERP Veterinária", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    for p in produtos:
        status = "Ativo" if p.ativo else "Inativo"
        pdf.cell(190, 10, f"Produto: {p.nome} | SKU: {p.sku} | Qtd: {p.quantidade_estoque} | Status: {status}", ln=True)
    
    pdf.output("relatorio_estoque.pdf")
    return "relatorio_estoque.pdf"

def gerar_relatorio_dre(dados_financeiros: dict):
    pdf = FPDF()
    pdf.add.page()

    #cabeçalho do DRE
    pdf.set_font("Arial", 'B', 16)
    pdf.cell (190, 10, "Demonstração do resultado do DRE", ln = True, align = 'C')
    pdf.set_font("Arial", size=12)
    pdf.cell(190, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln = True, align= 'C')
    pdf.ln(10)

    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "Descrição", border=1)
    pdf.cell(50, 10, "Valor(R$)", border=1, ln=True, align='C')

    pdf.set_font("Arial", size=12)

    pdf.cell(140, 10, "(+) Receita Bruta de vendas", border=1)
    pdf.cell(50, 10, f"{dados_financeiros['receita_total']:.2f}", border=1, ln=True, align='C')

    pdf.set_font("Arial", "I", 12)
    pdf.cell(140, 10, "(-) Impostos (Simples Nacional 10%)", border=1)
    pdf.cell(50, 10, f"-{dados_financeiros['impostos']:.2f}", border=1, ln=True, align='C')

    pdf.set_font("Arial",size = 12)
    pdf.cell(140, 10, "(-) Custo de Mercadoria / Despesas", border=1)
    pdf.cell(50, 10, f"-{dados_financeiros['despesas_totais']:.2f}", border=1, ln=True, align='C')

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    resultado = dados_financeiros['resultado_liquido']
    cor_texto = (0, 128, 0) if resultado >= 0 else (255, 0, 0) #RGB para lucro e prejuizo
    pdf.set_text_color(*cor_texto)

    pdf.cell(140, 12,, "LUCRO/PREJUÍZO LÍQUIDO:", border=0)
    pdf.cell(50, 12, f"R$ {resultado:.2f}",  border-=0, ln=True, align='R')

    pdf.output("relatorio_dre.pdf")
    return "relatorio_dre.pdf"