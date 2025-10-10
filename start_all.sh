#!/bin/bash

echo "🚀 Iniciando Óptica Solar..."

# Iniciar base de datos en background
echo "🗄️ Iniciando base de datos..."
docker-compose up -d database

# Esperar a que la base de datos esté lista
sleep 5

# Iniciar servidor de acciones en background
echo "⚡ Iniciando servidor de acciones..."
cd retailGPT/actions_server
poetry run python -m rasa_sdk --actions actions &
cd ../..

# Esperar a que el servidor de acciones esté listo
sleep 10

# Iniciar chatbot Rasa en background
echo "🤖 Iniciando chatbot Rasa..."
cd retailGPT/rasa_chatbot
poetry run rasa run &
cd ../..

# Esperar a que Rasa esté listo
sleep 15

# Iniciar interfaz de usuario
echo "🖥️ Iniciando interfaz de usuario..."
cd chat_interface/src
poetry run streamlit run app.py
