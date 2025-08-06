# Retail-GPT

Este repositorio contiene el código fuente de Retail-GPT, un chatbot de código abierto basado en RAG diseñado para guiar a los usuarios a través de recomendaciones de productos y ayudar con operaciones del carrito, con el objetivo de mejorar la interacción de los usuarios con el comercio electrónico minorista y servir como un agente de ventas virtual. El objetivo de este sistema es probar la viabilidad de un asistente de este tipo y proporcionar un marco adaptable para implementar chatbots de ventas en diferentes negocios minoristas.

Para propósitos de demostración y prueba, el chatbot implementado en este repositorio está contextualizado para funcionar como un agente de ventas para una tienda de conveniencia ficticia llamada Foo. Sin embargo, la implementación no depende de este dominio y podría adaptarse para trabajar con otro tipo de negocios.

El documento del proyecto puede leerse en [retailGPT PDF](/retailGPT.pdf)

El proyecto completo se compone de 4 aplicaciones diferentes que pueden ejecutarse por separado:

- **Interfaz de chat:** Aplicación de front-end para propósitos de demostración construida principalmente con [`Streamlit`](https://streamlit.io/). Esta aplicación es opcional, ya que el chatbot puede ejecutarse directamente desde la terminal.
- **Chatbot de Rasa:** Aplicación de [`Rasa`](https://rasa.com/) que sirve como base para todo el chatbot. Se encarga de procesar el chit-chat, extraer entidades y delegar tareas al subsistema RAG.
- **Servidor de acciones de Rasa:** Servidor de acciones personalizadas de [`Rasa`](https://rasa.com/) en el que se implementan las validaciones y el sistema RAG.
- **Base de datos Redis:** Base de datos para almacenar historiales de conversación y carritos de usuarios.

Para alimentar el sistema RAG implementado en el servidor de acciones, se utilizó el modelo `gpt-4o` de Open AI a través de la [`Open AI API`](https://openai.com/index/openai-api/) por su calidad de respuestas y su capacidad para realizar llamadas a funciones. Las llamadas a funciones son la característica principal utilizada para integrar el modelo con herramientas externas debido a su simplicidad de uso y efectividad, pero sería posible lograr resultados similares reemplazándolas con técnicas como ReAct prompting.

# Instalación y uso

## Interfaz de chat

Para instalar y ejecutar la interfaz de demostración del chatbot, sigue los pasos a continuación:

1. Clona el repositorio
2. Ejecuta `cd chat_interface` para ir al directorio de la interfaz
3. [Instala poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) para la gestión de dependencias
4. Instala las dependencias con `poetry install` en tu entorno activo actual (se recomienda usar un entorno de Python separado)
5. Ve a la carpeta de la aplicación con `cd src`
5. Ejecuta la aplicación de la interfaz con `streamlit run app.py`

La interfaz de demostración del chatbot estará disponible en http://localhost:8501. Puedes interactuar con el chatbot escribiendo mensajes en el cuadro de entrada y presionando Enter.

## Chatbot de Rasa

Para instalar las dependencias y ejecutar el chatbot:

1. Ejecuta `cd retailGPT/rasa_chatbot` para ir al directorio del chatbot de Rasa
2. Ejecuta `poetry install` para instalar las dependencias en tu entorno activo actual (se recomienda usar un entorno de Python separado)
3. Ejecuta `python -m spacy download en_core_web_lg` para descargar el modelo de [`spacy`](https://spacy.io/) utilizado
4. Ejecuta `rasa train` para entrenar el modelo
5. Ejecuta `rasa run` si deseas ejecutar la aplicación como una API.

De manera alternativa, en lugar de ejecutar `rasa run`, puedes ejecutar `rasa shell` (puedes añadir la opción `--debug` para obtener más registros) para ejecutar la aplicación e iniciar un chat directamente en la terminal. Esta opción puede ser útil si no deseas ejecutar la aplicación de interfaz por separado.

## Servidor de acciones de Rasa

Para instalar las dependencias y ejecutar el servidor de acciones:

1. Ejecuta `cd retailGPT/actions_server` para ir al directorio del servidor de acciones
2. Ejecuta `poetry install` para instalar las dependencias en tu entorno activo actual (se recomienda usar un entorno de Python separado)
3. Asegúrate de tener una variable de entorno `OPENAI_API_KEY` configurada con el valor de tu clave API
   1. Si prefieres usar Open AI a través de Microsoft Azure, asegúrate de editar el booleano `use_azure` en `llm_handler` a `True` y configura las siguientes variables de entorno:
       1. `AZURE_OPENAI_API_KEY`: clave para Azure Open AI
       2. `AZURE_RESOURCE`: recurso de Azure en el que se despliega el modelo
       3. `AZURE_API_VERSION`: versión del API del despliegue
4. Ejecuta `python -m rasa_sdk --actions actions` para ejecutar el servidor

## Base de datos

La base de datos se ejecuta como un contenedor de Redis. Para ejecutar la base de datos:

1. Asegúrate de tener [Docker]() instalado en tu máquina
2. Ejecuta `docker-compose up database`

La base de datos se ejecutará en el puerto 6379 y estará lista para ser utilizada por las otras aplicaciones.

## Ejecución con Docker

También puedes ejecutar todo mediante Docker utilizando el archivo compose en la raíz del proyecto. Ten en cuenta que, para que los contenedores se comuniquen entre sí en la red de Docker, también necesitarás actualizar los endpoints en el proyecto. En este sentido, haz lo siguiente:

En `chat_interface/src/chatbot.py`: Cambia "localhost" por "rasa" en las URL del chatbot de Rasa y "localhost" por "database" en la única URL relacionada con Redis.

En `retailGPT/rasa_chatbot/endpoints.tml`: Cambia "localhost" por "actions".

En `retailGPT/actions_server/src/LLMChatbot/services/chatbot.py`: Cambia "localhost" por "database".

## Arquitectura del código

Si es tu primera vez trabajando en este repositorio, probablemente necesitarás familiarizarte con los archivos y directorios listados a continuación. Ten en cuenta que no se listan todos los archivos del proyecto, solo los más importantes.

- `chat_interface`: Aplicación de interfaz
- `retailGPT`: Contiene toda la lógica del chatbot
  - `rasa_chatbot`: Proyecto de [`Rasa`](https://rasa.com/)
    - `endpoints.yml`: Contiene los endpoints para el bot, como el servidor de acciones y el tracker store.
    - `domain.yml`: Contiene el dominio del bot, incluyendo intents, entidades, acciones y respuestas.
    - `config.yml`: Pipeline de NLP utilizado por Rasa.
    - `data`
      - `nlu.yml`: Contiene los datos de entrenamiento de NLU.
      - `stories.yml`: Contiene las historias del bot.
      - `rules.yml`: Contiene las reglas del bot.
    - `models`: Contiene los modelos entrenados para clasificar intents y extraer slots.
  - `datasets`: Conjuntos de datos ficticios que se usan para pruebas y para proporcionar los productos disponibles en el comercio electrónico.
  - `actions_server`: Servidor de acciones personalizadas de [`Rasa`](https://rasa.com/)
    - `src`
      - `LLMChatbot`: implementa el subsistema basado en RAG
        - `chatbot.py`: Contiene el código del chatbot basado en LLM.
        - `prompts.py`: Contiene los prompts para el chatbot basado en LLM.
        - `services`
            - `database.py`: Contiene el código para el servicio de base de datos.
            - `product_handler.py`: Contiene el código para las funcionalidades relacionadas con productos.
            - `memory_handler.py`: Contiene el código para las funcionalidades relacionadas con memoria.
            - `cart_handler.py`: Contiene el código para las funcionalidades relacionadas con el carrito.
            - `llm_handler.py`: Contiene el código para las funcionalidades relacionadas con el LLM.
            - `guardrails`: Contiene la implementación de guardrails.
