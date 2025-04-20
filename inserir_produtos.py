import csv
import psycopg2

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    dbname="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y"
)
cursor = conn.cursor()

# Leitura do arquivo CSV salvo como produtos_final.csv
with open("produtos_final.csv", newline="", encoding="utf-8") as csvfile:
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
print("Produtos inseridos com sucesso.")
