import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "app", "static", "comprovantes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def gerar_comprovante_imagem(venda, cliente, itens):
    template = env.get_template("comprovante.html")
    html = template.render(venda=venda, cliente=cliente)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comprovante_{venda.id}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    hti = Html2Image(output_path=OUTPUT_DIR)
    hti.screenshot(html_str=html, save_as=filename, size=(800, 1000))

    return f"/static/comprovantes/{filename}"
