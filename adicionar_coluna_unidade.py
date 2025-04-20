import psycopg2

conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    database="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y"
)

cur = conn.cursor()

try:
    cur.execute("ALTER TABLE produtos ADD COLUMN unidade VARCHAR(50);")
    conn.commit()
    print("Coluna 'unidade' adicionada com sucesso.")
except Exception as e:
    print(f"Erro ao adicionar coluna 'unidade': {e}")

cur.close()
conn.close()
