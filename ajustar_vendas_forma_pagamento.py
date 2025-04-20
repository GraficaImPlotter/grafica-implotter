import psycopg2

conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    database="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y",
    port="5432"
)

cur = conn.cursor()

try:
    cur.execute("ALTER TABLE vendas ADD COLUMN forma_pagamento VARCHAR;")
    conn.commit()
    print("Coluna 'forma_pagamento' adicionada com sucesso!")
except psycopg2.errors.DuplicateColumn:
    print("A coluna 'forma_pagamento' já existe.")
finally:
    cur.close()
    conn.close()
