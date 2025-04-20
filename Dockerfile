# Dockerfile atualizado para Render

# Imagem base
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para dentro da imagem
COPY . .

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta que será usada (Render define automaticamente a porta via variável $PORT)
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com uvicorn, usando a porta fornecida pelo Render
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
