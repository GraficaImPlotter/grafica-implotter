import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "app", "static", "comprovantes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def gerar_comprovante_imagem(venda, cliente, itens):
    template = env.get_template("comprovante.html")
    html_content = template.render(venda=venda, cliente=cliente, itens=itens)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comprovante_{venda.id}_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    HTML(string=html_content).write_pdf(filepath)
    return f"/static/comprovantes/{filename}"