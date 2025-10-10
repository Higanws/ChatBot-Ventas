#!/usr/bin/env python3
"""
Test unitarios para ProductHandler de Óptica Solar
"""

import unittest
import json
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Agregar el path del proyecto
sys.path.append(str(Path(__file__).parent.parent / "retailGPT" / "actions_server" / "src"))

from LLMChatbot.services.product_handler import ProductHandler


class TestProductHandler(unittest.TestCase):
    """Test para ProductHandler"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.sample_products = {
            "products": [
                {
                    "row_id": 1,
                    "product_name": "Ray-Ban Aviator Classic Gold",
                    "brand": "Ray-Ban",
                    "model": "Aviator Classic",
                    "color": "Dorado",
                    "frame_material": "Metal",
                    "lens_type": "Polarizada",
                    "uv_protection": "100% UV400",
                    "size": "M",
                    "style": "Aviador",
                    "full_price": 299.99,
                    "image_url": "https://example.com/image.jpg",
                    "description": "Gafas aviador clásicas"
                },
                {
                    "row_id": 2,
                    "product_name": "Oakley Holbrook Matte Black",
                    "brand": "Oakley",
                    "model": "Holbrook",
                    "color": "Negro Mate",
                    "frame_material": "O Matter",
                    "lens_type": "Polarizada",
                    "uv_protection": "100% UV400",
                    "size": "M",
                    "style": "Wayfarer",
                    "full_price": 189.99,
                    "image_url": "https://example.com/image2.jpg",
                    "description": "Gafas deportivas"
                }
            ]
        }
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_product_catalog(self, mock_json_load, mock_file):
        """Test obtención de catálogo de productos"""
        mock_json_load.return_value = self.sample_products
        
        catalog = ProductHandler._get_product_catalog("12345678")
        
        self.assertIsInstance(catalog, str)
        self.assertIn("Ray-Ban Aviator Classic Gold", catalog)
        self.assertIn("Oakley Holbrook Matte Black", catalog)
        self.assertIn("R$299.99", catalog)
        self.assertIn("R$189.99", catalog)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_product_catalog_empty_zipcode(self, mock_json_load, mock_file):
        """Test catálogo con código postal que empieza en 0"""
        mock_json_load.return_value = self.sample_products
        
        catalog = ProductHandler._get_product_catalog("01234567")
        
        self.assertEqual(catalog, "")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_product_catalog_restricted_zipcode(self, mock_json_load, mock_file):
        """Test catálogo con código postal restringido"""
        mock_json_load.return_value = self.sample_products
        
        catalog = ProductHandler._get_product_catalog("91234567")
        
        # Solo debería incluir productos con índice % 3 == 0
        self.assertIn("Ray-Ban", catalog)  # índice 0
        self.assertNotIn("Oakley", catalog)  # índice 1
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_format_product_recommendation(self, mock_json_load, mock_file):
        """Test formateo de recomendaciones de productos"""
        mock_json_load.return_value = self.sample_products
        
        raw_recommendation = self.sample_products["products"][:1]
        formatted = ProductHandler._format_product_recommendation(raw_recommendation)
        
        self.assertIn("🕶️ Ray-Ban Aviator Classic Gold", formatted)
        self.assertIn("Marca: Ray-Ban", formatted)
        self.assertIn("Color: Dorado", formatted)
        self.assertIn("Estilo: Aviador", formatted)
        self.assertIn("Protección UV: 100% UV400", formatted)
        self.assertIn("Precio: R$299.99", formatted)
    
    def test_format_product_recommendation_empty(self):
        """Test formateo de recomendación vacía"""
        formatted = ProductHandler._format_product_recommendation([])
        
        self.assertEqual(formatted, "")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_purchase_history_dataset(self, mock_json_load, mock_file):
        """Test obtención de dataset de historial de compras"""
        sample_history = {
            "purchase_histories": [
                {"date": "2024-01-01", "products": ["Ray-Ban Aviator"]},
                {"date": "2024-01-02", "products": ["Oakley Holbrook"]}
            ]
        }
        mock_json_load.return_value = sample_history
        
        history = ProductHandler._get_purchase_history_dataset()
        
        self.assertEqual(len(history), 2)
        self.assertIn("Ray-Ban Aviator", history[0])
        self.assertIn("Oakley Holbrook", history[1])
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_purchase_history(self, mock_json_load, mock_file):
        """Test obtención de historial de compras por código postal"""
        sample_history = {
            "purchase_histories": [
                {"date": "2024-01-01", "products": ["Ray-Ban Aviator"]},
                {"date": "2024-01-02", "products": ["Oakley Holbrook"]},
                {"date": "2024-01-03", "products": ["Tom Ford"]}
            ]
        }
        mock_json_load.return_value = sample_history
        
        # Código postal que termina en 0
        history_0 = ProductHandler._get_purchase_history("12345670")
        self.assertIn("Ray-Ban Aviator", history_0)
        
        # Código postal que termina en 1
        history_1 = ProductHandler._get_purchase_history("12345671")
        self.assertIn("Oakley Holbrook", history_1)
        
        # Código postal que termina en 9 (fuera de rango)
        history_9 = ProductHandler._get_purchase_history("12345679")
        self.assertEqual(history_9, "")
    
    def test_product_was_recommended(self):
        """Test verificación si producto fue recomendado"""
        # Mock de datos de usuario
        user_data = {
            "recommended_products": [
                {
                    "product_name": "Ray-Ban Aviator Classic Gold",
                    "brand": "Ray-Ban",
                    "full_price": 299.99
                }
            ]
        }
        
        with patch.object(ProductHandler, '_get_recommendations_data', return_value=user_data["recommended_products"]):
            result = ProductHandler.product_was_recommended("user123", "Ray-Ban Aviator Classic Gold")
            self.assertTrue(result)
            
            result = ProductHandler.product_was_recommended("user123", "Oakley Holbrook")
            self.assertFalse(result)
    
    def test_get_product_unit_price(self):
        """Test obtención de precio unitario"""
        user_data = {
            "recommended_products": [
                {
                    "product_name": "Ray-Ban Aviator Classic Gold",
                    "brand": "Ray-Ban",
                    "full_price": 299.99
                }
            ]
        }
        
        with patch.object(ProductHandler, '_get_product_data', return_value=user_data["recommended_products"][0]):
            price = ProductHandler.get_product_unit_price("user123", "Ray-Ban Aviator Classic Gold")
            self.assertEqual(price, 299.99)
            
            price = ProductHandler.get_product_unit_price("user123", "Producto Inexistente")
            self.assertIsNone(price)
    
    def test_get_product_unit_volume(self):
        """Test obtención de volumen unitario"""
        user_data = {
            "recommended_products": [
                {
                    "product_name": "Ray-Ban Aviator Classic Gold",
                    "brand": "Ray-Ban",
                    "full_price": 299.99
                }
            ]
        }
        
        with patch.object(ProductHandler, '_get_product_data', return_value=user_data["recommended_products"][0]):
            volume = ProductHandler.get_product_unit_volume("user123", "Ray-Ban Aviator Classic Gold")
            self.assertEqual(volume, 0.001)  # Volumen fijo para gafas de sol
            
            volume = ProductHandler.get_product_unit_volume("user123", "Producto Inexistente")
            self.assertIsNone(volume)


if __name__ == '__main__':
    unittest.main()

