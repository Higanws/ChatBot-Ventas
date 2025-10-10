#!/usr/bin/env python3
"""
Script de instalación y configuración para Óptica Solar
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_poetry():
    """Verifica si Poetry está instalado"""
    try:
        result = subprocess.run(['poetry', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Poetry instalado: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Poetry no está instalado")
    print("📋 Instala Poetry desde: https://python-poetry.org/docs/#installing-with-the-official-installer")
    return False

def check_docker():
    """Verifica si Docker está instalado"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker instalado: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker no está instalado")
    print("📋 Instala Docker desde: https://docs.docker.com/get-docker/")
    return False

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\n🔧 Instalando dependencias...")
    
    # Instalar dependencias del servidor de acciones
    print("📦 Instalando dependencias del servidor de acciones...")
    try:
        os.chdir("retailGPT/actions_server")
        result = subprocess.run(['poetry', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencias del servidor de acciones instaladas")
        else:
            print(f"❌ Error instalando dependencias del servidor de acciones: {result.stderr}")
            return False
        os.chdir("../..")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Instalar dependencias del chatbot Rasa
    print("📦 Instalando dependencias del chatbot Rasa...")
    try:
        os.chdir("retailGPT/rasa_chatbot")
        result = subprocess.run(['poetry', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencias del chatbot Rasa instaladas")
        else:
            print(f"❌ Error instalando dependencias del chatbot Rasa: {result.stderr}")
            return False
        os.chdir("../..")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Instalar dependencias de la interfaz
    print("📦 Instalando dependencias de la interfaz...")
    try:
        os.chdir("chat_interface")
        result = subprocess.run(['poetry', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencias de la interfaz instaladas")
        else:
            print(f"❌ Error instalando dependencias de la interfaz: {result.stderr}")
            return False
        os.chdir("..")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def download_spacy_model():
    """Descarga el modelo de Spacy para español"""
    print("\n🤖 Descargando modelo de Spacy para español...")
    try:
        os.chdir("retailGPT/rasa_chatbot")
        result = subprocess.run(['python', '-m', 'spacy', 'download', 'es_core_news_lg'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Modelo de Spacy descargado")
        else:
            print(f"❌ Error descargando modelo de Spacy: {result.stderr}")
            return False
        os.chdir("../..")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def train_rasa_model():
    """Entrena el modelo de Rasa"""
    print("\n🧠 Entrenando modelo de Rasa...")
    try:
        os.chdir("retailGPT/rasa_chatbot")
        result = subprocess.run(['rasa', 'train'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Modelo de Rasa entrenado")
        else:
            print(f"❌ Error entrenando modelo de Rasa: {result.stderr}")
            return False
        os.chdir("../..")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def create_env_file():
    """Crea el archivo .env con las credenciales"""
    print("\n🔐 Configurando archivo de credenciales...")
    
    env_content = """# Configuración de Óptica Solar
# Configura tus credenciales aquí

# OpenAI API (REQUERIDO)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# MercadoPago (OPCIONAL - para pagos reales)
MERCADOPAGO_ACCESS_TOKEN=tu_clave_mercadopago_aqui

# Azure OpenAI (OPCIONAL - alternativa a OpenAI)
AZURE_OPENAI_API_KEY=tu_clave_azure_openai_aqui
AZURE_RESOURCE=tu_recurso_azure_aqui
AZURE_API_VERSION=2023-12-01-preview

# Base de datos Redis (para Docker)
REDIS_URL=redis://localhost:6379

# Configuración del chatbot
CHATBOT_NAME=Óptica Solar
CHATBOT_LANGUAGE=es

# URLs de la aplicación
RASA_URL=http://localhost:5005
ACTIONS_URL=http://localhost:5055
CHAT_INTERFACE_URL=http://localhost:8501
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    print("📝 Edita el archivo .env y configura tus credenciales")
    
    return True

def create_startup_scripts():
    """Crea scripts de inicio para cada componente"""
    print("\n🚀 Creando scripts de inicio...")
    
    # Script para iniciar la base de datos
    db_script = """#!/bin/bash
# Script para iniciar la base de datos Redis
echo "🗄️ Iniciando base de datos Redis..."
docker-compose up database
"""
    
    with open('start_database.sh', 'w') as f:
        f.write(db_script)
    
    # Script para iniciar el servidor de acciones
    actions_script = """#!/bin/bash
# Script para iniciar el servidor de acciones
echo "⚡ Iniciando servidor de acciones..."
cd retailGPT/actions_server
poetry run python -m rasa_sdk --actions actions
"""
    
    with open('start_actions.sh', 'w') as f:
        f.write(actions_script)
    
    # Script para iniciar el chatbot Rasa
    rasa_script = """#!/bin/bash
# Script para iniciar el chatbot Rasa
echo "🤖 Iniciando chatbot Rasa..."
cd retailGPT/rasa_chatbot
poetry run rasa run
"""
    
    with open('start_rasa.sh', 'w') as f:
        f.write(rasa_script)
    
    # Script para iniciar la interfaz
    ui_script = """#!/bin/bash
# Script para iniciar la interfaz de usuario
echo "🖥️ Iniciando interfaz de usuario..."
cd chat_interface/src
poetry run streamlit run app.py
"""
    
    with open('start_interface.sh', 'w') as f:
        f.write(ui_script)
    
    # Script para iniciar todo
    all_script = """#!/bin/bash
# Script para iniciar todo el sistema
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
"""
    
    with open('start_all.sh', 'w') as f:
        f.write(all_script)
    
    # Hacer los scripts ejecutables en sistemas Unix
    if os.name != 'nt':  # No es Windows
        os.chmod('start_database.sh', 0o755)
        os.chmod('start_actions.sh', 0o755)
        os.chmod('start_rasa.sh', 0o755)
        os.chmod('start_interface.sh', 0o755)
        os.chmod('start_all.sh', 0o755)
    
    print("✅ Scripts de inicio creados")
    
    return True

def main():
    """Función principal de configuración"""
    print("🕶️ Configurando Óptica Solar...")
    print("=" * 50)
    
    # Verificar prerrequisitos
    if not check_python_version():
        return False
    
    if not check_poetry():
        return False
    
    if not check_docker():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Descargar modelo de Spacy
    if not download_spacy_model():
        return False
    
    # Entrenar modelo de Rasa
    if not train_rasa_model():
        return False
    
    # Crear archivo de configuración
    if not create_env_file():
        return False
    
    # Crear scripts de inicio
    if not create_startup_scripts():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Edita el archivo .env y configura tus credenciales")
    print("2. Ejecuta: ./start_all.sh (Linux/Mac) o start_all.bat (Windows)")
    print("3. Abre http://localhost:8501 en tu navegador")
    print("\n🔐 Credenciales requeridas:")
    print("- OPENAI_API_KEY: Obtén tu clave en https://platform.openai.com/api-keys")
    print("- MERCADOPAGO_ACCESS_TOKEN: Obtén tu clave en https://www.mercadopago.com.ar/developers")
    
    return True

if __name__ == "__main__":
    main()
