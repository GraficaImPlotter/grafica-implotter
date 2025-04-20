import psycopg2

# Conexão com o banco do Render
conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    database="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y",
    port=5432
)

cur = conn.cursor()

# Tenta adicionar a coluna "total" se ela não existir
try:
    cur.execute("ALTER TABLE vendas ADD COLUMN total FLOAT;")
    conn.commit()
    print("Coluna 'total' adicionada com sucesso!")
except psycopg2.errors.DuplicateColumn:
    print("A coluna 'total' já existe.")
except Exception as e:
    print("Erro:", e)

cur.close()
conn.close()
