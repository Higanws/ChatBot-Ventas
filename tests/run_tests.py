#!/usr/bin/env python3
"""
Script para ejecutar todos los tests unitarios de Óptica Solar
"""

import unittest
import sys
from pathlib import Path

# Agregar el directorio de tests al path
sys.path.append(str(Path(__file__).parent))

def run_all_tests():
    """Ejecutar todos los tests unitarios"""
    print("🕶️ Ejecutando tests unitarios de Óptica Solar...")
    print("=" * 60)
    
    # Descubrir y ejecutar todos los tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 Resumen de Tests:")
    print(f"✅ Tests ejecutados: {result.testsRun}")
    print(f"❌ Fallos: {len(result.failures)}")
    print(f"⚠️ Errores: {len(result.errors)}")
    print(f"⏭️ Omitidos: {len(result.skipped)}")
    
    if result.failures:
        print("\n🔍 Fallos encontrados:")
        for test, traceback in result.failures:
            error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"  - {test}: {error_msg}")
    
    if result.errors:
        print("\n🚨 Errores encontrados:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")
    
    # Determinar si todos los tests pasaron
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ Óptica Solar está listo para usar")
    else:
        print("\n⚠️ Algunos tests fallaron")
        print("📝 Revisa los errores arriba y corrige los problemas")
    
    return success

def run_specific_test(test_name):
    """Ejecutar un test específico"""
    print(f"🔍 Ejecutando test específico: {test_name}")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        # Ejecutar test específico
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Ejecutar todos los tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
