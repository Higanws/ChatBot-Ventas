# Óptica Solar - Chatbot de Gafas de Sol

Este repositorio contiene el código fuente de Óptica Solar, un chatbot especializado en gafas de sol basado en RAG (Retrieval-Augmented Generation) diseñado para guiar a los usuarios a través de recomendaciones de gafas de sol, asesoramiento sobre protección UV, y asistencia con operaciones del carrito de compras.

## Características Principales

### 🕶️ Especialización en Gafas de Sol
- **Recomendaciones personalizadas** basadas en estilo, forma de cara, actividades y preferencias
- **Asesoramiento sobre protección UV** y tipos de lentes
- **Catálogo de marcas premium** como Ray-Ban, Oakley, Persol, Tom Ford, Gucci, Prada y Maui Jim
- **Filtros avanzados** por marca, color, material, estilo y protección UV

### 💳 Integración con MercadoPago
- **Procesamiento de pagos** seguro con MercadoPago
- **Múltiples métodos de pago** (tarjeta de crédito, débito, efectivo, MercadoPago)
- **Webhooks** para notificaciones de pago en tiempo real

### 🤖 Inteligencia Artificial Avanzada
- **Sistema RAG** con GPT-4o para recomendaciones inteligentes
- **Procesamiento de lenguaje natural** en español
- **Memoria de conversación** y historial de compras
- **Asesoramiento especializado** sobre cuidado y mantenimiento

## Arquitectura del Sistema

El proyecto está compuesto por 4 aplicaciones principales:

### 1. **Interfaz de Chat** (`chat_interface/`)
- Aplicación frontend construida con Streamlit
- Interfaz visual moderna para gafas de sol
- Integración con imágenes de productos
- Descarga de historial de conversaciones

### 2. **Chatbot Rasa** (`retailGPT/rasa_chatbot/`)
- Motor de conversación basado en Rasa
- Procesamiento de intents específicos para gafas de sol
- Extracción de entidades (estilo, color, marca, etc.)
- Gestión de formularios de compra

### 3. **Servidor de Acciones** (`retailGPT/actions_server/`)
- Lógica de negocio y sistema RAG
- Integración con MercadoPago
- Manejo de catálogo de productos
- Gestión de carrito de compras

### 4. **Base de Datos Redis**
- Almacenamiento de historiales de conversación
- Gestión de carritos de usuarios
- Cache de recomendaciones

## Instalación y Uso

### Prerrequisitos
- Python 3.8+
- Poetry para gestión de dependencias
- Docker para Redis
- Clave API de OpenAI
- Clave API de MercadoPago (opcional)

### 1. Interfaz de Chat
```bash
cd chat_interface
poetry install
cd src
streamlit run app.py
```

### 2. Chatbot Rasa
```bash
cd retailGPT/rasa_chatbot
poetry install
python -m spacy download es_core_news_lg
rasa train
rasa run
```

### 3. Servidor de Acciones
```bash
cd retailGPT/actions_server
poetry install
export OPENAI_API_KEY="tu_clave_api"
export MERCADOPAGO_ACCESS_TOKEN="tu_clave_mercadopago"  # opcional
python -m rasa_sdk --actions actions
```

### 4. Base de Datos
```bash
docker-compose up database
```

## Configuración de Variables de Entorno

```bash
# OpenAI API
export OPENAI_API_KEY="tu_clave_api_openai"

# MercadoPago (opcional)
export MERCADOPAGO_ACCESS_TOKEN="tu_clave_mercadopago"

# Azure OpenAI (alternativa)
export AZURE_OPENAI_API_KEY="tu_clave_azure"
export AZURE_RESOURCE="tu_recurso_azure"
export AZURE_API_VERSION="2023-12-01-preview"
```

## Funcionalidades del Chatbot

### 🎯 Recomendaciones Inteligentes
- **Por estilo**: Aviador, Wayfarer, Deportivo, Oversized
- **Por forma de cara**: Redonda, Ovalada, Cuadrada, Corazón
- **Por actividad**: Playa, Deporte, Ciudad, Conducir
- **Por marca**: Ray-Ban, Oakley, Tom Ford, Gucci, etc.

### 🛡️ Asesoramiento Técnico
- **Protección UV**: Explicación de UV400, 100% UV
- **Tipos de lentes**: Polarizadas, Espejadas, Degradadas
- **Materiales**: Acetato, Metal, Titanio
- **Cuidado y mantenimiento**: Limpieza, almacenamiento, garantía

### 🛒 Gestión de Compras
- **Búsqueda de productos** con filtros avanzados
- **Carrito de compras** con resumen detallado
- **Procesamiento de pagos** con MercadoPago
- **Seguimiento de pedidos** y confirmaciones

## Catálogo de Productos

El sistema incluye un catálogo completo de gafas de sol con:

- **20+ modelos** de marcas premium
- **Características detalladas**: Marca, modelo, color, material, protección UV
- **Precios realistas** en pesos argentinos
- **Imágenes de productos** para visualización
- **Descripciones técnicas** y de estilo

### Marcas Incluidas
- Ray-Ban (Aviator, Wayfarer, Clubmaster)
- Oakley (Holbrook, Flak, Radar)
- Persol (649, 714 Steve McQueen)
- Tom Ford (FT5235, FT5401)
- Gucci (GG0061S)
- Prada (PR 01VS)
- Maui Jim (Red Sands, Peahi)

## Personalización

### Agregar Nuevas Marcas
1. Actualizar `retailGPT/datasets/sunglasses_products.json`
2. Entrenar el modelo Rasa: `rasa train`
3. Reiniciar el servidor de acciones

### Modificar Prompts
1. Editar `retailGPT/actions_server/src/LLMChatbot/prompts.py`
2. Ajustar respuestas en `retailGPT/rasa_chatbot/domain.yml`
3. Entrenar el modelo: `rasa train`

### Integrar Nuevos Métodos de Pago
1. Extender `MercadoPagoHandler` en `mercadopago_handler.py`
2. Actualizar opciones de pago en `domain.yml`
3. Modificar interfaz de usuario

## Desarrollo

### Estructura de Archivos
```
├── chat_interface/          # Interfaz Streamlit
├── retailGPT/
│   ├── rasa_chatbot/        # Motor de conversación
│   ├── actions_server/      # Lógica de negocio
│   └── datasets/           # Catálogo de productos
├── docker-compose.yml      # Configuración Docker
└── README_OPTICA_SOLAR.md  # Este archivo
```

### Testing
```bash
# Entrenar modelo
cd retailGPT/rasa_chatbot
rasa train

# Probar conversación
rasa shell

# Ejecutar tests
rasa test
```

## Contribuciones

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas sobre el proyecto:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación de Rasa y OpenAI

---

**Óptica Solar** - Tu tienda especializada en gafas de sol de alta calidad 🕶️
