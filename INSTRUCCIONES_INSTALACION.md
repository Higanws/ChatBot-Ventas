# 🕶️ Óptica Solar - Instrucciones de Instalación

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.8+** - [Descargar Python](https://www.python.org/downloads/)
2. **Poetry** - [Instalar Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
3. **Docker** - [Instalar Docker](https://docs.docker.com/get-docker/)

## Instalación Automática

### Opción 1: Script Automático (Recomendado)

```bash
python setup_optica_solar.py
```

Este script:
- ✅ Verifica los prerrequisitos
- 📦 Instala todas las dependencias
- 🤖 Descarga el modelo de Spacy para español
- 🧠 Entrena el modelo de Rasa
- 🔐 Crea el archivo de configuración
- 🚀 Genera scripts de inicio

### Opción 2: Instalación Manual

#### 1. Instalar dependencias del servidor de acciones
```bash
cd retailGPT/actions_server
poetry install
cd ../..
```

#### 2. Instalar dependencias del chatbot Rasa
```bash
cd retailGPT/rasa_chatbot
poetry install
cd ../..
```

#### 3. Instalar dependencias de la interfaz
```bash
cd chat_interface
poetry install
cd ..
```

#### 4. Descargar modelo de Spacy
```bash
cd retailGPT/rasa_chatbot
python -m spacy download es_core_news_lg
cd ../..
```

#### 5. Entrenar modelo de Rasa
```bash
cd retailGPT/rasa_chatbot
rasa train
cd ../..
```

## Configuración de Credenciales

### 1. Crear archivo de configuración
```bash
cp env_example.txt .env
```

### 2. Editar el archivo .env
Abre el archivo `.env` y configura tus credenciales:

```env
# OpenAI API (REQUERIDO)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# MercadoPago (OPCIONAL - para pagos reales)
MERCADOPAGO_ACCESS_TOKEN=tu_clave_mercadopago_aqui
```

### 3. Obtener credenciales

#### OpenAI API Key
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crea una cuenta o inicia sesión
3. Haz clic en "Create new secret key"
4. Copia la clave y pégala en el archivo .env

#### MercadoPago Access Token (Opcional)
1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers)
2. Crea una cuenta o inicia sesión
3. Ve a "Credenciales"
4. Copia el "Access Token" y pégala en el archivo .env

## Ejecución del Sistema

### Opción 1: Inicio Automático (Recomendado)

#### Windows:
```bash
start_all.bat
```

#### Linux/Mac:
```bash
./start_all.sh
```

### Opción 2: Inicio Manual

Abre 4 terminales y ejecuta en cada una:

#### Terminal 1: Base de datos
```bash
docker-compose up database
```

#### Terminal 2: Servidor de acciones
```bash
cd retailGPT/actions_server
poetry run python -m rasa_sdk --actions actions
```

#### Terminal 3: Chatbot Rasa
```bash
cd retailGPT/rasa_chatbot
poetry run rasa run
```

#### Terminal 4: Interfaz de usuario
```bash
cd chat_interface/src
poetry run streamlit run app.py
```

## Acceso al Sistema

Una vez que todos los servicios estén ejecutándose:

1. **Interfaz de Usuario**: http://localhost:8501
2. **API de Rasa**: http://localhost:5005
3. **Servidor de Acciones**: http://localhost:5055
4. **Base de Datos Redis**: localhost:6379

## Verificación del Sistema

Ejecuta el script de prueba:
```bash
python test_optica_solar.py
```

## Solución de Problemas

### Error: "No module named 'pydantic'"
```bash
cd retailGPT/actions_server
poetry install
```

### Error: "No module named 'redis'"
```bash
cd retailGPT/actions_server
poetry install
```

### Error: "Model 'es_core_news_lg' not found"
```bash
cd retailGPT/rasa_chatbot
python -m spacy download es_core_news_lg
```

### Error: "Rasa model not trained"
```bash
cd retailGPT/rasa_chatbot
rasa train
```

### Error: "Docker not running"
- Inicia Docker Desktop
- Verifica que esté ejecutándose: `docker --version`

### Error: "Poetry not found"
- Instala Poetry: https://python-poetry.org/docs/#installing-with-the-official-installer
- Reinicia la terminal

## Estructura del Proyecto

```
├── chat_interface/          # Interfaz Streamlit
├── retailGPT/
│   ├── rasa_chatbot/        # Motor de conversación
│   ├── actions_server/      # Lógica de negocio
│   └── datasets/           # Catálogo de productos
├── docker-compose.yml      # Configuración Docker
├── .env                    # Credenciales (crear)
├── start_all.sh           # Script de inicio (Linux/Mac)
├── start_all.bat          # Script de inicio (Windows)
└── setup_optica_solar.py  # Script de instalación
```

## Soporte

Si tienes problemas:
1. Revisa los logs en cada terminal
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que las credenciales estén configuradas correctamente
4. Ejecuta el script de prueba para diagnosticar problemas

---

**¡Disfruta usando Óptica Solar! 🕶️✨**
