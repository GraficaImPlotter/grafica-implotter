#!/bin/bash

echo "⏳ Iniciando atualização do sistema da Gráfica Implotter..."

# Etapas do Git
git add .
git commit -m "Deploy automático - atualização de funcionalidades"
git push origin main

echo "✅ Atualização enviada ao GitHub com sucesso!"
echo "🚀 A Render irá iniciar o deploy automaticamente em alguns segundos."
