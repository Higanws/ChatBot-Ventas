# 🔐 Credenciales Requeridas para Óptica Solar

## Credenciales Obligatorias

### 1. OpenAI API Key (REQUERIDO)
**¿Qué es?** Clave para acceder a la API de OpenAI GPT-4o que potencia el sistema RAG del chatbot.

**¿Cómo obtenerla?**
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crea una cuenta o inicia sesión
3. Haz clic en "Create new secret key"
4. Copia la clave (comienza con `sk-`)
5. Pégala en el archivo `.env` como: `OPENAI_API_KEY=tu_clave_aqui`

**Costo:** Tiene un costo por uso, pero es muy económico para pruebas.

## Credenciales Opcionales

### 2. MercadoPago Access Token (OPCIONAL)
**¿Qué es?** Clave para procesar pagos reales con MercadoPago.

**¿Cómo obtenerla?**
1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers)
2. Crea una cuenta o inicia sesión
3. Ve a "Credenciales"
4. Copia el "Access Token"
5. Pégala en el archivo `.env` como: `MERCADOPAGO_ACCESS_TOKEN=tu_clave_aqui`

**Nota:** Sin esta credencial, el sistema funcionará pero no procesará pagos reales.

## Configuración del Archivo .env

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
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
```

## Pasos para Configurar

### 1. Crear archivo de configuración
```bash
cp env_example.txt .env
```

### 2. Editar el archivo .env
Abre el archivo `.env` con tu editor favorito y reemplaza:
- `tu_clave_api_openai_aqui` con tu clave real de OpenAI
- `tu_clave_mercadopago_aqui` con tu clave real de MercadoPago (opcional)

### 3. Verificar configuración
```bash
python test_simple.py
```

## Ejemplo de Configuración

```env
# Ejemplo de configuración real
OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef1234567890abcdef
MERCADOPAGO_ACCESS_TOKEN=APP_USR_1234567890abcdef1234567890abcdef
```

## Seguridad

⚠️ **IMPORTANTE:**
- Nunca compartas tus claves API
- No subas el archivo `.env` a repositorios públicos
- El archivo `.env` ya está en `.gitignore` para protegerlo

## Solución de Problemas

### Error: "Invalid API key"
- Verifica que la clave de OpenAI sea correcta
- Asegúrate de que no tenga espacios extra
- Verifica que la cuenta de OpenAI tenga créditos

### Error: "MercadoPago authentication failed"
- Verifica que la clave de MercadoPago sea correcta
- Asegúrate de que la cuenta esté activa
- Verifica que estés usando el Access Token correcto

### Error: "No API key configured"
- Verifica que el archivo `.env` exista
- Asegúrate de que las variables estén configuradas correctamente
- Reinicia el sistema después de cambiar las credenciales

## Soporte

Si tienes problemas con las credenciales:
1. Verifica que las claves sean correctas
2. Asegúrate de que las cuentas estén activas
3. Revisa los logs del sistema para más detalles
4. Consulta la documentación de OpenAI y MercadoPago

---

**¡Con estas credenciales configuradas, Óptica Solar estará listo para usar! 🕶️✨**
