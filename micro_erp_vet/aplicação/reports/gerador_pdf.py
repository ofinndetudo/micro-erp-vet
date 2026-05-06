from fpdf import FPDF
from aplica_o.models import Produto

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