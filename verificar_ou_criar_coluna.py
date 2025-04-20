from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://grafica_user:LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y@dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com/grafica"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='produtos' AND column_name='preco_venda';"))
    if result.fetchone():
        print("✅ A coluna 'preco_venda' já existe.")
    else:
        conn.execute(text("ALTER TABLE produtos ADD COLUMN preco_venda FLOAT;"))
        print("✅ Coluna 'preco_venda' foi criada com sucesso!")