@echo off
echo 🚀 Iniciando Óptica Solar...

REM Iniciar base de datos
echo 🗄️ Iniciando base de datos...
docker-compose up -d database

REM Esperar a que la base de datos esté lista
timeout /t 5 /nobreak >nul

REM Iniciar servidor de acciones
echo ⚡ Iniciando servidor de acciones...
cd retailGPT\actions_server
start "Servidor de Acciones" cmd /k "poetry run python -m rasa_sdk --actions actions"
cd ..\..

REM Esperar a que el servidor de acciones esté listo
timeout /t 10 /nobreak >nul

REM Iniciar chatbot Rasa
echo 🤖 Iniciando chatbot Rasa...
cd retailGPT\rasa_chatbot
start "Chatbot Rasa" cmd /k "poetry run rasa run"
cd ..\..

REM Esperar a que Rasa esté listo
timeout /t 15 /nobreak >nul

REM Iniciar interfaz de usuario
echo 🖥️ Iniciando interfaz de usuario...
cd chat_interface\src
start "Interfaz de Usuario" cmd /k "poetry run streamlit run app.py"
cd ..\..

echo ✅ Sistema iniciado. Abre http://localhost:8501 en tu navegador
pause
