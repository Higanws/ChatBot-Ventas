#!/usr/bin/env python3
"""
Script de prueba para Óptica Solar
Verifica la integración completa del sistema de gafas de sol
"""

import json
import requests
import time
from pathlib import Path

def test_sunglasses_catalog():
    """Prueba el catálogo de gafas de sol"""
    print("🕶️ Probando catálogo de gafas de sol...")
    
    catalog_path = Path("retailGPT/datasets/sunglasses_products.json")
    
    if not catalog_path.exists():
        print("❌ Error: No se encontró el catálogo de gafas de sol")
        return False
    
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    products = catalog.get("products", [])
    
    if len(products) == 0:
        print("❌ Error: El catálogo está vacío")
        return False
    
    print(f"✅ Catálogo cargado: {len(products)} productos")
    
    # Verificar estructura de productos
    required_fields = [
        "product_name", "brand", "model", "color", "frame_material",
        "lens_type", "uv_protection", "size", "style", "full_price",
        "image_url", "description"
    ]
    
    for i, product in enumerate(products[:3]):  # Verificar primeros 3 productos
        print(f"  Producto {i+1}: {product.get('product_name', 'Sin nombre')}")
        
        for field in required_fields:
            if field not in product:
                print(f"    ❌ Campo faltante: {field}")
                return False
            else:
                print(f"    ✅ {field}: {product[field]}")
    
    print("✅ Estructura del catálogo correcta")
    return True

def test_schemas():
    """Prueba los esquemas de productos"""
    print("\n📋 Probando esquemas de productos...")
    
    try:
        import sys
        sys.path.append("retailGPT/actions_server/src")
        from LLMChatbot.schemas import Product
        
        # Crear un producto de prueba
        test_product = Product(
            row_id=1,
            product_name="Test Sunglasses",
            brand="Test Brand",
            model="Test Model",
            color="Black",
            frame_material="Acetate",
            lens_type="Polarized",
            uv_protection="100% UV400",
            size="M",
            style="Wayfarer",
            full_price=199.99,
            image_url="https://example.com/test.jpg",
            description="Test sunglasses"
        )
        
        print("✅ Esquema de productos funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en esquemas: {e}")
        return False

def test_mercadopago_handler():
    """Prueba el manejador de MercadoPago"""
    print("\n💳 Probando integración con MercadoPago...")
    
    try:
        import sys
        sys.path.append("retailGPT/actions_server/src")
        from LLMChatbot.services.mercadopago_handler import MercadoPagoHandler
        
        handler = MercadoPagoHandler()
        payment_methods = handler.get_payment_methods()
        
        if len(payment_methods) == 0:
            print("❌ Error: No se encontraron métodos de pago")
            return False
        
        print(f"✅ Métodos de pago disponibles: {len(payment_methods)}")
        for method in payment_methods:
            print(f"  - {method['name']}: {method['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en MercadoPago: {e}")
        return False

def test_rasa_config():
    """Prueba la configuración de Rasa"""
    print("\n🤖 Probando configuración de Rasa...")
    
    config_path = Path("retailGPT/rasa_chatbot/config.yml")
    
    if not config_path.exists():
        print("❌ Error: No se encontró el archivo de configuración de Rasa")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    if "language: es" not in config_content:
        print("❌ Error: Idioma no configurado como español")
        return False
    
    if "es_core_news_lg" not in config_content:
        print("❌ Error: Modelo de Spacy no configurado para español")
        return False
    
    print("✅ Configuración de Rasa correcta")
    return True

def test_nlu_data():
    """Prueba los datos de entrenamiento NLU"""
    print("\n📝 Probando datos de entrenamiento NLU...")
    
    nlu_path = Path("retailGPT/rasa_chatbot/data/nlu.yml")
    
    if not nlu_path.exists():
        print("❌ Error: No se encontró el archivo NLU")
        return False
    
    with open(nlu_path, 'r', encoding='utf-8') as f:
        nlu_content = f.read()
    
    # Verificar intents específicos de gafas de sol
    sunglasses_intents = [
        "ask_style_recommendation",
        "ask_face_shape_advice", 
        "ask_uv_protection_info",
        "ask_brand_info",
        "ask_color_recommendation",
        "ask_activity_sunglasses",
        "ask_care_instructions"
    ]
    
    for intent in sunglasses_intents:
        if intent not in nlu_content:
            print(f"❌ Error: Intent faltante: {intent}")
            return False
        print(f"  ✅ Intent encontrado: {intent}")
    
    print("✅ Datos NLU correctos")
    return True

def test_domain_config():
    """Prueba la configuración del dominio"""
    print("\n🎯 Probando configuración del dominio...")
    
    domain_path = Path("retailGPT/rasa_chatbot/domain.yml")
    
    if not domain_path.exists():
        print("❌ Error: No se encontró el archivo de dominio")
        return False
    
    with open(domain_path, 'r', encoding='utf-8') as f:
        domain_content = f.read()
    
    # Verificar entidades específicas de gafas de sol
    sunglasses_entities = [
        "sunglasses_style",
        "face_shape",
        "activity_type",
        "brand_preference",
        "color_preference",
        "uv_protection"
    ]
    
    for entity in sunglasses_entities:
        if entity not in domain_content:
            print(f"❌ Error: Entidad faltante: {entity}")
            return False
        print(f"  ✅ Entidad encontrada: {entity}")
    
    # Verificar respuestas en español
    if "Óptica Solar" not in domain_content:
        print("❌ Error: Respuestas no actualizadas para Óptica Solar")
        return False
    
    print("✅ Configuración del dominio correcta")
    return True

def test_ui_config():
    """Prueba la configuración de la interfaz de usuario"""
    print("\n🖥️ Probando configuración de la interfaz...")
    
    app_path = Path("chat_interface/src/app.py")
    
    if not app_path.exists():
        print("❌ Error: No se encontró el archivo de la interfaz")
        return False
    
    with open(app_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    if "Óptica Solar" not in app_content:
        print("❌ Error: Interfaz no actualizada para Óptica Solar")
        return False
    
    if "gafas de sol" not in app_content.lower():
        print("❌ Error: Contenido de gafas de sol no encontrado en la interfaz")
        return False
    
    print("✅ Configuración de la interfaz correcta")
    return True

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas de Óptica Solar...")
    print("=" * 50)
    
    tests = [
        test_sunglasses_catalog,
        test_schemas,
        test_mercadopago_handler,
        test_rasa_config,
        test_nlu_data,
        test_domain_config,
        test_ui_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error inesperado en {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Óptica Solar está listo para usar.")
        print("\n📋 Próximos pasos:")
        print("1. Configurar variables de entorno (OPENAI_API_KEY, MERCADOPAGO_ACCESS_TOKEN)")
        print("2. Instalar dependencias: poetry install")
        print("3. Entrenar modelo Rasa: rasa train")
        print("4. Ejecutar servicios: docker-compose up")
        print("5. Iniciar interfaz: streamlit run app.py")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    main()
