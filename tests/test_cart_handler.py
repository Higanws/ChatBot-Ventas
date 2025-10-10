#!/usr/bin/env python3
"""
Test unitarios para CartHandler de Óptica Solar
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch

# Agregar el path del proyecto
sys.path.append(str(Path(__file__).parent.parent / "retailGPT" / "actions_server" / "src"))

from LLMChatbot.services.cart_handler import CartHandler


class TestCartHandler(unittest.TestCase):
    """Test para CartHandler"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.user_id = "test_user_123"
        self.sample_cart = [
            {
                "product_name": "Ray-Ban Aviator Classic Gold",
                "number_of_units": 2,
                "price_per_unit": 299.99,
                "volume_per_unit": 0.001
            },
            {
                "product_name": "Oakley Holbrook Matte Black",
                "number_of_units": 1,
                "price_per_unit": 189.99,
                "volume_per_unit": 0.001
            }
        ]
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_set_cart(self, mock_database):
        """Test establecer carrito"""
        mock_database.get_data.return_value = {}
        
        CartHandler._set_cart(self.user_id, self.sample_cart)
        
        mock_database.set_data.assert_called_once()
        call_args = mock_database.set_data.call_args[0]
        self.assertEqual(call_args[0], self.user_id)
        self.assertEqual(call_args[1]["cart"], self.sample_cart)
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_get_cart(self, mock_database):
        """Test obtener carrito"""
        mock_database.get_data.return_value = {"cart": self.sample_cart}
        
        cart = CartHandler._get_cart(self.user_id)
        
        self.assertEqual(cart, self.sample_cart)
        mock_database.get_data.assert_called_once_with(self.user_id)
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_get_cart_empty(self, mock_database):
        """Test obtener carrito vacío"""
        mock_database.get_data.return_value = {}
        
        cart = CartHandler._get_cart(self.user_id)
        
        self.assertEqual(cart, [])
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_get_cart_summary(self, mock_database):
        """Test obtener resumen del carrito"""
        mock_database.get_data.return_value = {"cart": self.sample_cart}
        
        summary = CartHandler.get_cart_summary(self.user_id)
        
        self.assertIn("Your cart summary:", summary)
        self.assertIn("Ray-Ban Aviator Classic Gold", summary)
        self.assertIn("Oakley Holbrook Matte Black", summary)
        self.assertIn("2 units", summary)
        self.assertIn("1 unit", summary)
        self.assertIn("R$789.97", summary)  # Total: (299.99 * 2) + 189.99
        self.assertIn("Total cart volume: 0.003L", summary)
        self.assertIn("Métodos de pago disponibles", summary)
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_get_cart_summary_empty(self, mock_database):
        """Test resumen de carrito vacío"""
        mock_database.get_data.return_value = {}
        
        summary = CartHandler.get_cart_summary(self.user_id)
        
        self.assertIn("Your cart summary:", summary)
        self.assertIn("Total cart value: R$0.00", summary)
        self.assertIn("Total cart volume: 0L", summary)
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_get_should_send_cart_summary(self, mock_database):
        """Test obtener flag de envío de resumen"""
        mock_database.get_data.return_value = {"should_send_cart_summary": True}
        
        result = CartHandler.get_should_send_cart_summary(self.user_id)
        
        self.assertTrue(result)
    
    @patch('LLMChatbot.services.cart_handler.Database')
    def test_set_should_send_cart_summary(self, mock_database):
        """Test establecer flag de envío de resumen"""
        mock_database.get_data.return_value = {}
        
        CartHandler.set_should_send_cart_summary(self.user_id, True)
        
        mock_database.set_data.assert_called_once()
        call_args = mock_database.set_data.call_args[0]
        self.assertEqual(call_args[0], self.user_id)
        self.assertEqual(call_args[1]["should_send_cart_summary"], True)
    
    def test_add_to_cart_new_product(self):
        """Test agregar producto nuevo al carrito"""
        cart = []
        
        CartHandler._add_to_cart(
            cart, "Tom Ford FT5235 Negro", 1, 499.99, 0.001
        )
        
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]["product_name"], "Tom Ford FT5235 Negro")
        self.assertEqual(cart[0]["number_of_units"], 1)
        self.assertEqual(cart[0]["price_per_unit"], 499.99)
    
    def test_add_to_cart_existing_product(self):
        """Test agregar producto existente al carrito"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 1,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        CartHandler._add_to_cart(
            cart, "Ray-Ban Aviator Classic Gold", 2, 299.99, 0.001
        )
        
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]["number_of_units"], 3)  # 1 + 2
    
    def test_max_volume_exceeded(self):
        """Test verificación de volumen máximo excedido"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 3,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        # Volumen actual: 3 * 0.001 = 0.003
        # Volumen adicional: 3 * 0.001 = 0.003
        # Total: 0.006, que excede el máximo de 5
        result = CartHandler._max_volume_exceeded(cart, 3 * 0.001)
        
        self.assertFalse(result)  # No excede el máximo de 5L
    
    def test_max_volume_exceeded_true(self):
        """Test verificación de volumen máximo excedido (caso verdadero)"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 3000,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        # Volumen actual: 3000 * 0.001 = 3
        # Volumen adicional: 3000 * 0.001 = 3
        # Total: 6, que excede el máximo de 5
        result = CartHandler._max_volume_exceeded(cart, 3000 * 0.001)
        
        self.assertTrue(result)
    
    def test_get_max_allowed_units(self):
        """Test obtener máximo de unidades permitidas"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 2000,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        # Volumen actual: 2000 * 0.001 = 2
        # Volumen restante: 5 - 2 = 3
        # Unidades máximas: 3 / 0.001 = 3000
        max_units = CartHandler._get_max_allowed_units(cart, 0.001)
        
        self.assertEqual(max_units, 3000)
    
    @patch('LLMChatbot.services.cart_handler.ProductHandler')
    @patch('LLMChatbot.services.cart_handler.CartHandler._add_to_cart')
    @patch('LLMChatbot.services.cart_handler.CartHandler._max_volume_exceeded')
    @patch('LLMChatbot.services.cart_handler.CartHandler._get_max_allowed_units')
    def test_process_addition_success(self, mock_get_max, mock_volume_exceeded, mock_add_to_cart, mock_product_handler):
        """Test procesamiento de adición exitosa"""
        mock_product_handler.get_product_unit_price.return_value = 299.99
        mock_product_handler.get_product_unit_volume.return_value = 0.001
        mock_volume_exceeded.return_value = False
        
        result = CartHandler._process_addition(self.user_id, [], "Ray-Ban Aviator", 2)
        
        self.assertEqual(result, "Product successfully added to the cart!")
        mock_add_to_cart.assert_called_once()
    
    @patch('LLMChatbot.services.cart_handler.ProductHandler')
    @patch('LLMChatbot.services.cart_handler.CartHandler._add_to_cart')
    @patch('LLMChatbot.services.cart_handler.CartHandler._max_volume_exceeded')
    @patch('LLMChatbot.services.cart_handler.CartHandler._get_max_allowed_units')
    def test_process_addition_volume_exceeded(self, mock_get_max, mock_volume_exceeded, mock_add_to_cart, mock_product_handler):
        """Test procesamiento de adición con volumen excedido"""
        mock_product_handler.get_product_unit_price.return_value = 299.99
        mock_product_handler.get_product_unit_volume.return_value = 0.001
        mock_volume_exceeded.return_value = True
        mock_get_max.return_value = 1
        
        result = CartHandler._process_addition(self.user_id, [], "Ray-Ban Aviator", 5)
        
        self.assertIn("The maximum volume of 5 liters per order has been exceeded", result)
        self.assertIn("adjusted to 1", result)
        mock_add_to_cart.assert_called_once()
    
    def test_process_removal_success(self):
        """Test procesamiento de eliminación exitosa"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 3,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        result = CartHandler._process_removal(cart, "Ray-Ban Aviator Classic Gold", 1)
        
        self.assertEqual(result, "Product units successfully removed from the cart!")
        self.assertEqual(cart[0]["number_of_units"], 2)
    
    def test_process_removal_complete(self):
        """Test procesamiento de eliminación completa"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 2,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        result = CartHandler._process_removal(cart, "Ray-Ban Aviator Classic Gold", 2)
        
        self.assertEqual(result, "Product units successfully removed from the cart!")
        self.assertEqual(len(cart), 0)  # Producto eliminado completamente
    
    def test_process_removal_below_zero(self):
        """Test procesamiento de eliminación por debajo de cero"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 1,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        result = CartHandler._process_removal(cart, "Ray-Ban Aviator Classic Gold", 3)
        
        self.assertEqual(result, "The number of units to remove is greater than the number of units in the cart. Therefore, this operation only completely removed the product.")
        self.assertEqual(len(cart), 0)
    
    def test_process_removal_product_not_found(self):
        """Test procesamiento de eliminación de producto no encontrado"""
        cart = [{
            "product_name": "Ray-Ban Aviator Classic Gold",
            "number_of_units": 1,
            "price_per_unit": 299.99,
            "volume_per_unit": 0.001
        }]
        
        result = CartHandler._process_removal(cart, "Producto Inexistente", 1)
        
        self.assertEqual(result, "Product not found in the cart.")
    
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_addition')
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_removal')
    @patch('LLMChatbot.services.cart_handler.CartHandler._set_cart')
    def test_process_cart_operation_add(self, mock_set_cart, mock_process_removal, mock_process_addition):
        """Test procesamiento de operación de carrito - agregar"""
        mock_process_addition.return_value = "Product successfully added to the cart!"
        
        result = CartHandler.process_cart_operation(self.user_id, "add", "Ray-Ban Aviator", 2)
        
        self.assertEqual(result, "Product successfully added to the cart!")
        mock_process_addition.assert_called_once_with(self.user_id, [], "Ray-Ban Aviator", 2)
        mock_set_cart.assert_called_once()
    
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_addition')
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_removal')
    @patch('LLMChatbot.services.cart_handler.CartHandler._set_cart')
    def test_process_cart_operation_remove(self, mock_set_cart, mock_process_removal, mock_process_addition):
        """Test procesamiento de operación de carrito - eliminar"""
        mock_process_removal.return_value = "Product units successfully removed from the cart!"
        
        result = CartHandler.process_cart_operation(self.user_id, "remove", "Ray-Ban Aviator", 1)
        
        self.assertEqual(result, "Product units successfully removed from the cart!")
        mock_process_removal.assert_called_once_with([], "Ray-Ban Aviator", 1)
        mock_set_cart.assert_called_once()
    
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_addition')
    @patch('LLMChatbot.services.cart_handler.CartHandler._process_removal')
    @patch('LLMChatbot.services.cart_handler.CartHandler._set_cart')
    def test_process_cart_operation_invalid(self, mock_set_cart, mock_process_removal, mock_process_addition):
        """Test procesamiento de operación de carrito - operación inválida"""
        result = CartHandler.process_cart_operation(self.user_id, "invalid", "Ray-Ban Aviator", 1)
        
        self.assertEqual(result, "Invalid operation")
        mock_process_addition.assert_not_called()
        mock_process_removal.assert_not_called()
        mock_set_cart.assert_called_once()


if __name__ == '__main__':
    unittest.main()

