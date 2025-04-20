import psycopg2

# Dados da conexão (já conhecidos)
conn = psycopg2.connect(
    host="dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com",
    port=5432,
    database="grafica",
    user="grafica_user",
    password="LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y"
)

cur = conn.cursor()

# Comando para alterar o nome da coluna
try:
    cur.execute("""
        ALTER TABLE vendas RENAME COLUMN forma_pagamento TO forma_pagto;
    """)
    conn.commit()
    print("Coluna renomeada com sucesso!")
except Exception as e:
    print("Erro ao renomear a coluna:", e)
finally:
    cur.close()
    conn.close()