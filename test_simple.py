#!/usr/bin/env python3
"""
Test simple para verificar que Óptica Solar está listo para usar
"""

import os
import json
from pathlib import Path

def test_environment():
    """Verifica que el entorno esté configurado correctamente"""
    print("Verificando entorno...")
    
    # Verificar archivos principales
    required_files = [
        "retailGPT/datasets/sunglasses_products.json",
        "retailGPT/rasa_chatbot/config.yml",
        "retailGPT/rasa_chatbot/domain.yml",
        "retailGPT/actions_server/src/LLMChatbot/schemas.py",
        "chat_interface/src/app.py",
        "docker-compose.yml"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"ERROR: Archivo faltante: {file_path}")
            return False
        print(f"OK: {file_path}")
    
    return True

def test_catalog():
    """Verifica el catálogo de productos"""
    print("\nVerificando catálogo de gafas de sol...")
    
    catalog_path = Path("retailGPT/datasets/sunglasses_products.json")
    
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    products = catalog.get("products", [])
    
    if len(products) == 0:
        print("ERROR: Catálogo vacío")
        return False
    
    print(f"OK: Catálogo con {len(products)} productos")
    
    # Verificar marcas
    brands = set(product.get("brand", "") for product in products)
    print(f"OK: Marcas: {', '.join(sorted(brands))}")
    
    return True

def test_rasa_config():
    """Verifica la configuración de Rasa"""
    print("\nVerificando configuración de Rasa...")
    
    config_path = Path("retailGPT/rasa_chatbot/config.yml")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    if "language: es" not in config_content:
        print("ERROR: Idioma no configurado como español")
        return False
    
    if "es_core_news_lg" not in config_content:
        print("ERROR: Modelo de Spacy no configurado para español")
        return False
    
    print("OK: Configuración de Rasa correcta")
    return True

def test_scripts():
    """Verifica los scripts de inicio"""
    print("\nVerificando scripts de inicio...")
    
    scripts = [
        "start_all.bat",
        "start_all.sh",
        "setup_optica_solar.py"
    ]
    
    for script in scripts:
        if not Path(script).exists():
            print(f"ERROR: Script faltante: {script}")
            return False
        print(f"OK: {script}")
    
    return True

def main():
    """Función principal de verificación"""
    print("Verificación final de Óptica Solar")
    print("=" * 50)
    
    tests = [
        ("Entorno", test_environment),
        ("Catálogo", test_catalog),
        ("Rasa", test_rasa_config),
        ("Scripts", test_scripts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"ERROR en {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Resultados: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("\n¡Óptica Solar está listo para usar!")
        print("\nPara iniciar el sistema:")
        print("   Windows: start_all.bat")
        print("   Linux/Mac: ./start_all.sh")
        print("\nLuego abre: http://localhost:8501")
        
        print("\nCredenciales requeridas:")
        print("1. OPENAI_API_KEY - Obtén en: https://platform.openai.com/api-keys")
        print("2. MERCADOPAGO_ACCESS_TOKEN - Obtén en: https://www.mercadopago.com.ar/developers")
        
        print("\nFuncionalidades disponibles:")
        print("- Recomendaciones de gafas de sol")
        print("- Asesoramiento sobre protección UV")
        print("- Carrito de compras")
        print("- Integración con MercadoPago")
        print("- Interfaz en español")
        
    else:
        print("\nAlgunas verificaciones fallaron")
        print("Revisa los errores arriba y corrige los problemas")
    
    return passed == total

if __name__ == "__main__":
    main()
