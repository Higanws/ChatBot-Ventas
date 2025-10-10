#!/usr/bin/env python3
"""
Test unitarios para los esquemas de Óptica Solar
"""

import unittest
import sys
from pathlib import Path

# Agregar el path del proyecto
sys.path.append(str(Path(__file__).parent.parent / "retailGPT" / "actions_server" / "src"))

from LLMChatbot.schemas import Product, ChatbotResponse, RasaButton


class TestProductSchema(unittest.TestCase):
    """Test para el esquema de Product"""
    
    def test_product_creation(self):
        """Test creación de producto válido"""
        product = Product(
            row_id=1,
            product_name="Ray-Ban Aviator Classic Gold",
            brand="Ray-Ban",
            model="Aviator Classic",
            color="Dorado",
            frame_material="Metal",
            lens_type="Polarizada",
            uv_protection="100% UV400",
            size="M",
            style="Aviador",
            full_price=299.99,
            image_url="https://example.com/image.jpg",
            description="Gafas aviador clásicas"
        )
        
        self.assertEqual(product.row_id, 1)
        self.assertEqual(product.product_name, "Ray-Ban Aviator Classic Gold")
        self.assertEqual(product.brand, "Ray-Ban")
        self.assertEqual(product.full_price, 299.99)
        self.assertEqual(product.uv_protection, "100% UV400")
    
    def test_product_validation(self):
        """Test validación de campos requeridos"""
        with self.assertRaises(ValueError):
            Product(
                row_id=1,
                product_name="Test",
                # Faltan campos requeridos
            )


class TestRasaButtonSchema(unittest.TestCase):
    """Test para el esquema de RasaButton"""
    
    def test_button_creation(self):
        """Test creación de botón válido"""
        button = RasaButton(
            title="Sí, soy mayor de edad",
            payload="/affirm"
        )
        
        self.assertEqual(button.title, "Sí, soy mayor de edad")
        self.assertEqual(button.payload, "/affirm")
    
    def test_button_validation(self):
        """Test validación de botón"""
        with self.assertRaises(ValueError):
            RasaButton(
                # Faltan campos requeridos
            )


class TestChatbotResponseSchema(unittest.TestCase):
    """Test para el esquema de ChatbotResponse"""
    
    def test_response_creation(self):
        """Test creación de respuesta válida"""
        buttons = [
            RasaButton(title="Opción 1", payload="/option1"),
            RasaButton(title="Opción 2", payload="/option2")
        ]
        
        response = ChatbotResponse(
            text="¿Qué opción prefieres?",
            buttons=buttons
        )
        
        self.assertEqual(response.text, "¿Qué opción prefieres?")
        self.assertEqual(len(response.buttons), 2)
        self.assertEqual(response.buttons[0].title, "Opción 1")
    
    def test_response_without_buttons(self):
        """Test respuesta sin botones"""
        response = ChatbotResponse(
            text="Respuesta simple",
            buttons=[]
        )
        
        self.assertEqual(response.text, "Respuesta simple")
        self.assertEqual(len(response.buttons), 0)


if __name__ == '__main__':
    unittest.main()

