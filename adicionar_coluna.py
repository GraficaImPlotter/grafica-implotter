from sqlalchemy import create_engine, text

# URL externa do banco PostgreSQL (Render)
DATABASE_URL = "postgresql://grafica_user:LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y@dpg-d01orl3uibrs73b19lv0-p.elephantsql.render.com:5432/grafica"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE produtos ADD COLUMN preco_venda FLOAT;"))
    print("✅ Coluna 'preco_venda' adicionada com sucesso!")