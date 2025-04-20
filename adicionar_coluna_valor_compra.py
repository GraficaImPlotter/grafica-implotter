from sqlalchemy import create_engine, text

# Substitua sua URL correta abaixo:
DATABASE_URL = "postgresql://grafica_user:LJDHFaBekl1HpDUOaUxDbW00lN0Pgf9Y@dpg-d01orl3uibrs73b19lv0-a.oregon-postgres.render.com/grafica"
engine = create_engine(DATABASE_URL)

def adicionar_coluna(nome_coluna, tipo_sql):
    with engine.connect() as conn:
        try:
            conn.execute(text(f'ALTER TABLE produtos ADD COLUMN {nome_coluna} {tipo_sql}'))
            print(f"Coluna '{nome_coluna}' adicionada com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar coluna '{nome_coluna}': {e}")

if __name__ == "__main__":
    adicionar_coluna("valor_compra", "FLOAT")
    adicionar_coluna("preco_venda", "FLOAT")
