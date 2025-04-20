import psycopg2
import csv

# Conexão com o banco PostgreSQL na Render
conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    port=5432,
    database="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y"
)

cursor = conn.cursor()

# Abrir e ler o arquivo CSV
with open("produtos.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nome = row["nome"]
        descricao = row["descricao"]
        valor_compra = float(row["valor_compra"])
        preco_venda = float(row["preco_venda"])
        unidade = row["unidade"]

        cursor.execute("""
            INSERT INTO produtos (nome, descricao, valor_compra, preco_venda, unidade)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nome) DO NOTHING;
        """, (nome, descricao, valor_compra, preco_venda, unidade))

conn.commit()
cursor.close()
conn.close()

print("Importação concluída com sucesso.")
