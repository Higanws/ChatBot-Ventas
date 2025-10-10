# 🕶️ Óptica Solar - Chatbot de Gafas de Sol

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Rasa](https://img.shields.io/badge/Rasa-3.x-red.svg)](https://rasa.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-green.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple.svg)](https://openai.com)
[![MercadoPago](https://img.shields.io/badge/MercadoPago-API-yellow.svg)](https://mercadopago.com)

> **Sistema de chatbot inteligente especializado en gafas de sol con recomendaciones personalizadas, asesoramiento sobre protección UV y procesamiento de pagos integrado.**

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación Rápida](#-instalación-rápida)
- [Instalación Detallada](#-instalación-detallada)
- [Configuración](#-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Testing](#-testing)
- [API y Endpoints](#-api-y-endpoints)
- [Desarrollo](#-desarrollo)
- [Despliegue](#-despliegue)
- [Troubleshooting](#-troubleshooting)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

## 🌟 Características Principales

### 🕶️ **Especialización en Gafas de Sol**
- **Recomendaciones inteligentes** basadas en IA con GPT-4o
- **Asesoramiento personalizado** según estilo, forma de cara y actividades
- **Catálogo premium** con marcas como Ray-Ban, Oakley, Tom Ford, Gucci, Prada
- **Filtros avanzados** por marca, color, material, estilo y protección UV

### 💳 **Integración de Pagos**
- **Procesamiento seguro** con MercadoPago
- **Múltiples métodos de pago** (tarjeta, débito, efectivo, MercadoPago)
- **Webhooks en tiempo real** para notificaciones de pago
- **Carrito inteligente** con validaciones de volumen y stock

### 🤖 **Inteligencia Artificial Avanzada**
- **Sistema RAG** (Retrieval-Augmented Generation) con GPT-4o
- **Procesamiento de lenguaje natural** en español
- **Memoria de conversación** y historial de compras
- **Asesoramiento técnico** sobre protección UV y cuidado

### 🎨 **Interfaz de Usuario**
- **Interfaz moderna** construida con Streamlit
- **Diseño responsivo** y fácil de usar
- **Visualización de productos** con imágenes
- **Descarga de historial** de conversaciones

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interfaz      │    │   Chatbot       │    │  Servidor de    │
│   Streamlit     │◄──►│   Rasa          │◄──►│  Acciones       │
│   (Frontend)    │    │   (NLP Engine)  │    │  (Business Logic)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Descarga      │    │   Redis         │    │   OpenAI        │
│   Conversaciones│    │   Database      │    │   GPT-4o        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   MercadoPago   │
                       │   API           │
                       └─────────────────┘
```

### **Componentes Principales:**

1. **Interfaz Streamlit** (`chat_interface/`)
   - Frontend interactivo
   - Visualización de productos
   - Gestión de conversaciones

2. **Chatbot Rasa** (`retailGPT/rasa_chatbot/`)
   - Motor de conversación
   - Procesamiento de NLP
   - Gestión de intents y entidades

3. **Servidor de Acciones** (`retailGPT/actions_server/`)
   - Lógica de negocio
   - Sistema RAG
   - Integración con APIs externas

4. **Base de Datos Redis**
   - Almacenamiento de sesiones
   - Cache de recomendaciones
   - Gestión de carritos

## 🚀 Instalación Rápida

### **Prerrequisitos:**
- Python 3.8+
- Poetry
- Docker
- Clave API de OpenAI

### **Instalación Automática:**

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd ChatBot-Ventas

# 2. Instalar automáticamente
python setup_optica_solar.py

# 3. Configurar credenciales
cp env_example.txt .env
# Edita .env con tus credenciales

# 4. Ejecutar sistema
start_all.bat  # Windows
./start_all.sh # Linux/Mac
```

### **Acceso:**
- **Interfaz de Usuario:** http://localhost:8501
- **API de Rasa:** http://localhost:5005
- **Servidor de Acciones:** http://localhost:5055

## 📖 Instalación Detallada

### **1. Verificar Prerrequisitos**

```bash
# Verificar Python
python --version  # Debe ser 3.8+

# Verificar Poetry
poetry --version

# Verificar Docker
docker --version
```

### **2. Instalación Manual**

#### **Servidor de Acciones:**
```bash
cd retailGPT/actions_server
poetry install
cd ../..
```

#### **Chatbot Rasa:**
```bash
cd retailGPT/rasa_chatbot
poetry install
python -m spacy download es_core_news_lg
rasa train
cd ../..
```

#### **Interfaz de Usuario:**
```bash
cd chat_interface
poetry install
cd ..
```

#### **Base de Datos:**
```bash
docker-compose up -d database
```

### **3. Configuración de Variables de Entorno**

Crear archivo `.env`:
```env
# OpenAI API (REQUERIDO)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# MercadoPago (OPCIONAL)
MERCADOPAGO_ACCESS_TOKEN=tu_clave_mercadopago_aqui

# Configuración
CHATBOT_NAME=Óptica Solar
CHATBOT_LANGUAGE=es
```

### **4. Entrenamiento del Modelo**

```bash
cd retailGPT/rasa_chatbot
rasa train
cd ../..
```

## ⚙️ Configuración

### **Credenciales Requeridas:**

#### **OpenAI API Key (OBLIGATORIO)**
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crea una cuenta o inicia sesión
3. Haz clic en "Create new secret key"
4. Copia la clave y pégala en `.env`

#### **MercadoPago Access Token (OPCIONAL)**
1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers)
2. Crea una cuenta o inicia sesión
3. Ve a "Credenciales"
4. Copia el "Access Token" y pégala en `.env`

### **Configuración Avanzada:**

#### **Personalizar Catálogo:**
```bash
# Editar catálogo de productos
nano retailGPT/datasets/sunglasses_products.json

# Reentrenar modelo
cd retailGPT/rasa_chatbot
rasa train
```

#### **Modificar Prompts:**
```bash
# Editar prompts del chatbot
nano retailGPT/actions_server/src/LLMChatbot/prompts.py
```

#### **Configurar Idiomas:**
```bash
# Cambiar idioma en config.yml
nano retailGPT/rasa_chatbot/config.yml
```

## 🎯 Uso del Sistema

### **Flujo de Usuario Típico:**

1. **Saludo y Verificación:**
   - El chatbot saluda al usuario
   - Verifica edad legal
   - Solicita código postal

2. **Recomendaciones:**
   - Usuario describe sus necesidades
   - Sistema recomienda gafas de sol
   - Muestra características y precios

3. **Carrito de Compras:**
   - Usuario agrega productos al carrito
   - Sistema valida disponibilidad
   - Muestra resumen del carrito

4. **Procesamiento de Pago:**
   - Usuario selecciona método de pago
   - Sistema procesa con MercadoPago
   - Confirma la compra

### **Comandos Útiles:**

```bash
# Ver estado del sistema
python test_simple.py

# Ejecutar tests unitarios
python tests/run_tests.py

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicios
docker-compose restart
```

## 🧪 Testing

### **Tests Unitarios:**

```bash
# Ejecutar todos los tests
python tests/run_tests.py

# Ejecutar test específico
python tests/run_tests.py test_schemas

# Ejecutar con cobertura
python -m pytest tests/ --cov=retailGPT
```

### **Tests Disponibles:**

- **`test_schemas.py`** - Esquemas de datos
- **`test_product_handler.py`** - Manejo de productos
- **`test_cart_handler.py`** - Manejo de carrito
- **`test_mercadopago_handler.py`** - Integración MercadoPago
- **`test_catalog.py`** - Catálogo de productos
- **`test_rasa_config.py`** - Configuración de Rasa

### **Verificación del Sistema:**

```bash
# Verificar instalación
python test_simple.py

# Verificar configuración
python -c "import os; print('OK' if os.getenv('OPENAI_API_KEY') else 'Falta OPENAI_API_KEY')"
```

## 🔌 API y Endpoints

### **Endpoints Principales:**

#### **Rasa API:**
- `POST /webhooks/rest/webhook` - Enviar mensaje
- `GET /conversations/{conversation_id}/tracker` - Estado de conversación
- `POST /conversations/{conversation_id}/execute` - Ejecutar acción

#### **Servidor de Acciones:**
- `POST /webhook` - Webhook de Rasa
- `GET /health` - Estado del servidor

#### **Interfaz Streamlit:**
- `GET /` - Interfaz principal
- `GET /download_conversation` - Descargar conversación

### **Ejemplo de Uso de API:**

```python
import requests

# Enviar mensaje al chatbot
response = requests.post(
    "http://localhost:5005/webhooks/rest/webhook",
    json={
        "sender": "user123",
        "message": "Quiero gafas aviador para la playa"
    }
)

print(response.json())
```

## 🛠️ Desarrollo

### **Estructura del Proyecto:**

```
├── chat_interface/          # Interfaz Streamlit
│   ├── src/
│   │   ├── app.py          # Aplicación principal
│   │   ├── chatbot.py      # Cliente del chatbot
│   │   └── utils/          # Utilidades
│   └── pyproject.toml      # Dependencias
├── retailGPT/
│   ├── rasa_chatbot/       # Motor de conversación
│   │   ├── config.yml      # Configuración Rasa
│   │   ├── domain.yml      # Dominio del bot
│   │   └── data/           # Datos de entrenamiento
│   ├── actions_server/     # Lógica de negocio
│   │   └── src/
│   │       └── LLMChatbot/
│   │           ├── schemas.py      # Esquemas de datos
│   │           ├── prompts.py      # Prompts del LLM
│   │           └── services/       # Servicios
│   └── datasets/           # Catálogo de productos
├── tests/                  # Tests unitarios
├── docker-compose.yml      # Configuración Docker
└── README.md              # Este archivo
```

### **Agregar Nuevas Funcionalidades:**

#### **1. Nuevo Intent:**
```yaml
# En retailGPT/rasa_chatbot/data/nlu.yml
- intent: ask_warranty_info
  examples: |
    - What is the warranty?
    - How long is the warranty?
    - What warranty do you offer?
```

#### **2. Nueva Acción:**
```python
# En retailGPT/actions_server/src/actions.py
class ActionWarrantyInfo(Action):
    def name(self) -> Text:
        return "action_warranty_info"
    
    def run(self, dispatcher, tracker, domain):
        # Lógica de la acción
        pass
```

#### **3. Nuevo Producto:**
```json
// En retailGPT/datasets/sunglasses_products.json
{
  "row_id": 21,
  "product_name": "Nuevo Modelo",
  "brand": "Nueva Marca",
  "model": "Nuevo Modelo",
  "color": "Nuevo Color",
  "frame_material": "Nuevo Material",
  "lens_type": "Nuevo Tipo",
  "uv_protection": "100% UV400",
  "size": "M",
  "style": "Nuevo Estilo",
  "full_price": 199.99,
  "image_url": "https://example.com/image.jpg",
  "description": "Descripción del nuevo producto"
}
```

### **Debugging:**

```bash
# Logs detallados de Rasa
cd retailGPT/rasa_chatbot
rasa run --debug

# Logs del servidor de acciones
cd retailGPT/actions_server
poetry run python -m rasa_sdk --actions actions --debug

# Logs de Docker
docker-compose logs -f
```

## 🚀 Despliegue

### **Despliegue Local:**

```bash
# Usar Docker Compose
docker-compose up -d

# Verificar servicios
docker-compose ps
```

### **Despliegue en Producción:**

#### **1. Configurar Variables de Entorno:**
```bash
export OPENAI_API_KEY="tu_clave_produccion"
export MERCADOPAGO_ACCESS_TOKEN="tu_clave_produccion"
export ENVIRONMENT="production"
```

#### **2. Usar Docker Compose:**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  rasa:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    ports:
      - "5005:5005"
  
  actions:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MERCADOPAGO_ACCESS_TOKEN=${MERCADOPAGO_ACCESS_TOKEN}
    ports:
      - "5055:5055"
  
  demo:
    build: .
    ports:
      - "8501:8501"
  
  database:
    image: redis:alpine
    ports:
      - "6379:6379"
```

#### **3. Desplegar:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **Monitoreo:**

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Verificar estado de servicios
curl http://localhost:5005/health
curl http://localhost:5055/health

# Métricas de uso
docker stats
```

## 🔧 Troubleshooting

### **Problemas Comunes:**

#### **Error: "No module named 'pydantic'"**
```bash
cd retailGPT/actions_server
poetry install
```

#### **Error: "Model 'es_core_news_lg' not found"**
```bash
cd retailGPT/rasa_chatbot
python -m spacy download es_core_news_lg
```

#### **Error: "Rasa model not trained"**
```bash
cd retailGPT/rasa_chatbot
rasa train
```

#### **Error: "Docker not running"**
```bash
# Iniciar Docker Desktop
# Verificar que esté ejecutándose
docker --version
```

#### **Error: "Poetry not found"**
```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -
# Reiniciar terminal
```

#### **Error: "OpenAI API key not configured"**
```bash
# Verificar archivo .env
cat .env
# Configurar clave
export OPENAI_API_KEY="tu_clave_aqui"
```

### **Logs Útiles:**

```bash
# Logs de Rasa
tail -f retailGPT/rasa_chatbot/rasa.log

# Logs del servidor de acciones
tail -f retailGPT/actions_server/actions.log

# Logs de Docker
docker-compose logs -f
```

### **Verificación del Sistema:**

```bash
# Test completo
python test_simple.py

# Test específico
python tests/run_tests.py test_catalog

# Verificar servicios
curl http://localhost:5005/health
curl http://localhost:5055/health
curl http://localhost:8501
```

## 🤝 Contribuciones

### **Cómo Contribuir:**

1. **Fork del repositorio**
2. **Crear rama de feature:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Hacer cambios y tests:**
   ```bash
   python tests/run_tests.py
   ```
4. **Commit de cambios:**
   ```bash
   git commit -am 'Agregar nueva funcionalidad'
   ```
5. **Push a la rama:**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
6. **Crear Pull Request**

### **Estándares de Código:**

- **Python:** PEP 8
- **Tests:** Cobertura mínima 80%
- **Documentación:** Docstrings en español
- **Commits:** Mensajes descriptivos

### **Áreas de Contribución:**

- 🐛 **Bug fixes**
- ✨ **Nuevas funcionalidades**
- 📚 **Documentación**
- 🧪 **Tests**
- 🎨 **Mejoras de UI/UX**
- 🔧 **Optimizaciones**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

### **Recursos de Ayuda:**

- 📖 **Documentación:** [README_OPTICA_SOLAR.md](README_OPTICA_SOLAR.md)
- 🔧 **Instalación:** [INSTRUCCIONES_INSTALACION.md](INSTRUCCIONES_INSTALACION.md)
- 🔐 **Credenciales:** [CREDENCIALES_REQUERIDAS.md](CREDENCIALES_REQUERIDAS.md)

### **Contacto:**

- 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/ChatBot-Ventas/issues)
- 💬 **Discusiones:** [GitHub Discussions](https://github.com/tu-usuario/ChatBot-Ventas/discussions)
- 📧 **Email:** soporte@opticasolar.com

### **Comunidad:**

- 👥 **Discord:** [Servidor de Discord](https://discord.gg/opticasolar)
- 📺 **YouTube:** [Canal de Tutoriales](https://youtube.com/opticasolar)
- 🐦 **Twitter:** [@OpticaSolar](https://twitter.com/opticasolar)

---

**¡Gracias por usar Óptica Solar! 🕶️✨**

*Desarrollado con ❤️ para la comunidad de desarrolladores de chatbots.*

