#!/usr/bin/env python3
"""
Test unitarios para MercadoPagoHandler de Óptica Solar
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar el path del proyecto
sys.path.append(str(Path(__file__).parent.parent / "retailGPT" / "actions_server" / "src"))

from LLMChatbot.services.mercadopago_handler import MercadoPagoHandler


class TestMercadoPagoHandler(unittest.TestCase):
    """Test para MercadoPagoHandler"""
    
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
        self.zipcode = "12345678"
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    def test_init_with_token(self):
        """Test inicialización con token"""
        handler = MercadoPagoHandler()
        
        self.assertEqual(handler.access_token, "test_token")
        self.assertEqual(handler.base_url, "https://api.mercadopago.com")
        self.assertIn("Authorization", handler.headers)
        self.assertIn("Bearer test_token", handler.headers["Authorization"])
    
    @patch.dict('os.environ', {}, clear=True)
    def test_init_without_token(self):
        """Test inicialización sin token"""
        handler = MercadoPagoHandler()
        
        self.assertIsNone(handler.access_token)
    
    def test_calculate_total_amount(self):
        """Test cálculo de monto total"""
        handler = MercadoPagoHandler()
        
        total = handler._calculate_total_amount(self.sample_cart)
        
        expected_total = (299.99 * 2) + 189.99  # 789.97
        self.assertEqual(total, expected_total)
    
    def test_calculate_total_amount_empty_cart(self):
        """Test cálculo de monto total con carrito vacío"""
        handler = MercadoPagoHandler()
        
        total = handler._calculate_total_amount([])
        
        self.assertEqual(total, 0.0)
    
    def test_create_items_from_cart(self):
        """Test creación de items de MercadoPago desde carrito"""
        handler = MercadoPagoHandler()
        
        items = handler._create_items_from_cart(self.sample_cart)
        
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "Ray-Ban Aviator Classic Gold")
        self.assertEqual(items[0]["quantity"], 2)
        self.assertEqual(items[0]["unit_price"], 299.99)
        self.assertEqual(items[0]["currency_id"], "ARS")
        self.assertEqual(items[1]["title"], "Oakley Holbrook Matte Black")
        self.assertEqual(items[1]["quantity"], 1)
        self.assertEqual(items[1]["unit_price"], 189.99)
    
    def test_create_items_from_cart_empty(self):
        """Test creación de items con carrito vacío"""
        handler = MercadoPagoHandler()
        
        items = handler._create_items_from_cart([])
        
        self.assertEqual(len(items), 0)
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('requests.post')
    def test_create_payment_preference_no_token(self, mock_post):
        """Test creación de preferencia de pago sin token"""
        handler = MercadoPagoHandler()
        
        result = handler.create_payment_preference(self.user_id, self.sample_cart, self.zipcode)
        
        self.assertFalse(result["success"])
        self.assertIn("MercadoPago access token not configured", result["error"])
        mock_post.assert_not_called()
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.post')
    def test_create_payment_preference_success(self, mock_post):
        """Test creación de preferencia de pago exitosa"""
        # Mock de respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "test_preference_id",
            "init_point": "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=test_preference_id",
            "sandbox_init_point": "https://sandbox.mercadopago.com.ar/checkout/v1/redirect?pref_id=test_preference_id"
        }
        mock_post.return_value = mock_response
        
        handler = MercadoPagoHandler()
        result = handler.create_payment_preference(self.user_id, self.sample_cart, self.zipcode)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["preference_id"], "test_preference_id")
        self.assertIn("init_point", result)
        self.assertIn("sandbox_init_point", result)
        self.assertEqual(result["total_amount"], 789.97)
        
        # Verificar que se llamó a la API con los datos correctos
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://api.mercadopago.com/checkout/preferences")
        self.assertIn("Authorization", call_args[1]["headers"])
        self.assertIn("items", call_args[1]["json"])
        self.assertIn("payer", call_args[1]["json"])
        self.assertIn("back_urls", call_args[1]["json"])
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.post')
    def test_create_payment_preference_api_error(self, mock_post):
        """Test creación de preferencia de pago con error de API"""
        # Mock de respuesta con error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        handler = MercadoPagoHandler()
        result = handler.create_payment_preference(self.user_id, self.sample_cart, self.zipcode)
        
        self.assertFalse(result["success"])
        self.assertIn("MercadoPago API error: 400", result["error"])
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.post')
    def test_create_payment_preference_exception(self, mock_post):
        """Test creación de preferencia de pago con excepción"""
        mock_post.side_effect = Exception("Network error")
        
        handler = MercadoPagoHandler()
        result = handler.create_payment_preference(self.user_id, self.sample_cart, self.zipcode)
        
        self.assertFalse(result["success"])
        self.assertIn("Error creating payment preference: Network error", result["error"])
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('requests.get')
    def test_get_payment_status_no_token(self, mock_get):
        """Test obtención de estado de pago sin token"""
        handler = MercadoPagoHandler()
        
        result = handler.get_payment_status("test_payment_id")
        
        self.assertFalse(result["success"])
        self.assertIn("MercadoPago access token not configured", result["error"])
        mock_get.assert_not_called()
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.get')
    def test_get_payment_status_success(self, mock_get):
        """Test obtención de estado de pago exitosa"""
        # Mock de respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "test_payment_id",
            "status": "approved",
            "status_detail": "accredited",
            "transaction_amount": 789.97,
            "currency_id": "ARS"
        }
        mock_get.return_value = mock_response
        
        handler = MercadoPagoHandler()
        result = handler.get_payment_status("test_payment_id")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["status_detail"], "accredited")
        self.assertEqual(result["transaction_amount"], 789.97)
        self.assertEqual(result["currency_id"], "ARS")
        
        # Verificar que se llamó a la API con la URL correcta
        mock_get.assert_called_once_with(
            "https://api.mercadopago.com/v1/payments/test_payment_id",
            headers=handler.headers
        )
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.get')
    def test_get_payment_status_error(self, mock_get):
        """Test obtención de estado de pago con error"""
        # Mock de respuesta con error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        handler = MercadoPagoHandler()
        result = handler.get_payment_status("invalid_payment_id")
        
        self.assertFalse(result["success"])
        self.assertIn("Error getting payment status: 404", result["error"])
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch('requests.get')
    def test_get_payment_status_exception(self, mock_get):
        """Test obtención de estado de pago con excepción"""
        mock_get.side_effect = Exception("Network error")
        
        handler = MercadoPagoHandler()
        result = handler.get_payment_status("test_payment_id")
        
        self.assertFalse(result["success"])
        self.assertIn("Error getting payment status: Network error", result["error"])
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch.object(MercadoPagoHandler, 'get_payment_status')
    def test_process_payment_webhook_approved(self, mock_get_status):
        """Test procesamiento de webhook con pago aprobado"""
        mock_get_status.return_value = {
            "success": True,
            "status": "approved",
            "status_detail": "accredited",
            "transaction_amount": 789.97,
            "currency_id": "ARS"
        }
        
        webhook_data = {
            "data": {"id": "test_payment_id"}
        }
        
        handler = MercadoPagoHandler()
        result = handler.process_payment_webhook(webhook_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "approved")
        self.assertIn("Payment approved, order processed", result["message"])
        mock_get_status.assert_called_once_with("test_payment_id")
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch.object(MercadoPagoHandler, 'get_payment_status')
    def test_process_payment_webhook_rejected(self, mock_get_status):
        """Test procesamiento de webhook con pago rechazado"""
        mock_get_status.return_value = {
            "success": True,
            "status": "rejected",
            "status_detail": "cc_rejected_insufficient_amount",
            "transaction_amount": 789.97,
            "currency_id": "ARS"
        }
        
        webhook_data = {
            "data": {"id": "test_payment_id"}
        }
        
        handler = MercadoPagoHandler()
        result = handler.process_payment_webhook(webhook_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["message"], "Payment rejected")
    
    @patch.dict('os.environ', {'MERCADOPAGO_ACCESS_TOKEN': 'test_token'})
    @patch.object(MercadoPagoHandler, 'get_payment_status')
    def test_process_payment_webhook_pending(self, mock_get_status):
        """Test procesamiento de webhook con pago pendiente"""
        mock_get_status.return_value = {
            "success": True,
            "status": "pending",
            "status_detail": "pending_waiting_payment",
            "transaction_amount": 789.97,
            "currency_id": "ARS"
        }
        
        webhook_data = {
            "data": {"id": "test_payment_id"}
        }
        
        handler = MercadoPagoHandler()
        result = handler.process_payment_webhook(webhook_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["message"], "Payment status: pending")
    
    def test_process_payment_webhook_no_payment_id(self):
        """Test procesamiento de webhook sin ID de pago"""
        webhook_data = {
            "data": {}
        }
        
        handler = MercadoPagoHandler()
        result = handler.process_payment_webhook(webhook_data)
        
        self.assertFalse(result["success"])
        self.assertIn("No payment ID in webhook data", result["error"])
    
    def test_process_payment_webhook_exception(self):
        """Test procesamiento de webhook con excepción"""
        webhook_data = {
            "data": {"id": "test_payment_id"}
        }
        
        handler = MercadoPagoHandler()
        
        with patch.object(handler, 'get_payment_status', side_effect=Exception("API error")):
            result = handler.process_payment_webhook(webhook_data)
            
            self.assertFalse(result["success"])
            self.assertIn("Error processing webhook: API error", result["error"])
    
    def test_get_payment_methods(self):
        """Test obtención de métodos de pago"""
        methods = MercadoPagoHandler.get_payment_methods()
        
        self.assertEqual(len(methods), 4)
        
        # Verificar MercadoPago
        mercadopago_method = next(m for m in methods if m["id"] == "mercadopago")
        self.assertEqual(mercadopago_method["name"], "MercadoPago")
        self.assertIn("tarjetas, efectivo, transferencia", mercadopago_method["description"])
        self.assertEqual(mercadopago_method["icon"], "💳")
        
        # Verificar tarjeta de crédito
        credit_method = next(m for m in methods if m["id"] == "credit_card")
        self.assertEqual(credit_method["name"], "Tarjeta de Crédito")
        self.assertEqual(credit_method["icon"], "💳")
        
        # Verificar tarjeta de débito
        debit_method = next(m for m in methods if m["id"] == "debit_card")
        self.assertEqual(debit_method["name"], "Tarjeta de Débito")
        self.assertEqual(debit_method["icon"], "💳")
        
        # Verificar efectivo
        cash_method = next(m for m in methods if m["id"] == "cash")
        self.assertEqual(cash_method["name"], "Efectivo")
        self.assertEqual(cash_method["icon"], "💵")


if __name__ == '__main__':
    unittest.main()

