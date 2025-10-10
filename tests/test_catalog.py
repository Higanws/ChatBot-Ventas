#!/usr/bin/env python3
"""
Test unitarios para el catálogo de gafas de sol de Óptica Solar
"""

import unittest
import json
from pathlib import Path


class TestSunglassesCatalog(unittest.TestCase):
    """Test para el catálogo de gafas de sol"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.catalog_path = Path("retailGPT/datasets/sunglasses_products.json")
        self.load_catalog()
    
    def load_catalog(self):
        """Cargar el catálogo de productos"""
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            self.catalog = json.load(f)
        self.products = self.catalog.get("products", [])
    
    def test_catalog_structure(self):
        """Test estructura del catálogo"""
        self.assertIn("products", self.catalog)
        self.assertIsInstance(self.catalog["products"], list)
        self.assertGreater(len(self.products), 0)
    
    def test_catalog_not_empty(self):
        """Test que el catálogo no esté vacío"""
        self.assertGreater(len(self.products), 0, "El catálogo no puede estar vacío")
    
    def test_product_structure(self):
        """Test estructura de cada producto"""
        required_fields = [
            "row_id", "product_name", "brand", "model", "color",
            "frame_material", "lens_type", "uv_protection", "size",
            "style", "full_price", "image_url", "description"
        ]
        
        for product in self.products:
            for field in required_fields:
                self.assertIn(field, product, f"Campo '{field}' faltante en producto {product.get('product_name', 'Unknown')}")
                self.assertIsNotNone(product[field], f"Campo '{field}' no puede ser None en producto {product.get('product_name', 'Unknown')}")
    
    def test_product_data_types(self):
        """Test tipos de datos de cada producto"""
        for product in self.products:
            # row_id debe ser entero
            self.assertIsInstance(product["row_id"], int, f"row_id debe ser entero en producto {product.get('product_name', 'Unknown')}")
            
            # product_name debe ser string
            self.assertIsInstance(product["product_name"], str, f"product_name debe ser string en producto {product.get('product_name', 'Unknown')}")
            self.assertGreater(len(product["product_name"]), 0, f"product_name no puede estar vacío en producto {product.get('product_name', 'Unknown')}")
            
            # brand debe ser string
            self.assertIsInstance(product["brand"], str, f"brand debe ser string en producto {product.get('product_name', 'Unknown')}")
            self.assertGreater(len(product["brand"]), 0, f"brand no puede estar vacío en producto {product.get('product_name', 'Unknown')}")
            
            # full_price debe ser float
            self.assertIsInstance(product["full_price"], (int, float), f"full_price debe ser numérico en producto {product.get('product_name', 'Unknown')}")
            self.assertGreater(product["full_price"], 0, f"full_price debe ser positivo en producto {product.get('product_name', 'Unknown')}")
            
            # image_url debe ser string válido
            self.assertIsInstance(product["image_url"], str, f"image_url debe ser string en producto {product.get('product_name', 'Unknown')}")
            self.assertIn("http", product["image_url"], f"image_url debe ser una URL válida en producto {product.get('product_name', 'Unknown')}")
    
    def test_unique_row_ids(self):
        """Test que los row_id sean únicos"""
        row_ids = [product["row_id"] for product in self.products]
        self.assertEqual(len(row_ids), len(set(row_ids)), "Los row_id deben ser únicos")
    
    def test_unique_product_names(self):
        """Test que los nombres de productos sean únicos"""
        product_names = [product["product_name"] for product in self.products]
        self.assertEqual(len(product_names), len(set(product_names)), "Los nombres de productos deben ser únicos")
    
    def test_brands_in_catalog(self):
        """Test marcas presentes en el catálogo"""
        expected_brands = ["Ray-Ban", "Oakley", "Persol", "Tom Ford", "Gucci", "Prada", "Maui Jim"]
        actual_brands = list(set(product["brand"] for product in self.products))
        
        for brand in expected_brands:
            self.assertIn(brand, actual_brands, f"Marca '{brand}' no encontrada en el catálogo")
    
    def test_styles_in_catalog(self):
        """Test estilos presentes en el catálogo"""
        expected_styles = ["Aviador", "Wayfarer", "Deportivo", "Oversized", "Redondo", "Clubmaster"]
        actual_styles = list(set(product["style"] for product in self.products))
        
        for style in expected_styles:
            self.assertIn(style, actual_styles, f"Estilo '{style}' no encontrado en el catálogo")
    
    def test_colors_in_catalog(self):
        """Test colores presentes en el catálogo"""
        expected_colors = ["Negro", "Dorado", "Plateado", "Marrón", "Tortuga", "Azul"]
        actual_colors = list(set(product["color"] for product in self.products))
        
        for color in expected_colors:
            self.assertIn(color, actual_colors, f"Color '{color}' no encontrado en el catálogo")
    
    def test_frame_materials_in_catalog(self):
        """Test materiales de montura presentes en el catálogo"""
        expected_materials = ["Metal", "Acetato", "O Matter", "Titanio"]
        actual_materials = list(set(product["frame_material"] for product in self.products))
        
        for material in expected_materials:
            self.assertIn(material, actual_materials, f"Material '{material}' no encontrado en el catálogo")
    
    def test_lens_types_in_catalog(self):
        """Test tipos de lente presentes en el catálogo"""
        expected_lens_types = ["Polarizada", "Cristal", "Espejada", "Degradada"]
        actual_lens_types = list(set(product["lens_type"] for product in self.products))
        
        for lens_type in expected_lens_types:
            self.assertIn(lens_type, actual_lens_types, f"Tipo de lente '{lens_type}' no encontrado en el catálogo")
    
    def test_uv_protection_in_catalog(self):
        """Test protección UV en el catálogo"""
        for product in self.products:
            self.assertIn("100%", product["uv_protection"], f"Protección UV debe ser 100% en producto {product.get('product_name', 'Unknown')}")
            self.assertIn("UV", product["uv_protection"], f"Protección UV debe mencionar UV en producto {product.get('product_name', 'Unknown')}")
    
    def test_sizes_in_catalog(self):
        """Test tallas presentes en el catálogo"""
        expected_sizes = ["S", "M", "L"]
        actual_sizes = list(set(product["size"] for product in self.products))
        
        for size in expected_sizes:
            self.assertIn(size, actual_sizes, f"Talla '{size}' no encontrada en el catálogo")
    
    def test_price_range(self):
        """Test rango de precios"""
        prices = [product["full_price"] for product in self.products]
        
        self.assertGreater(min(prices), 0, "El precio mínimo debe ser mayor a 0")
        self.assertLess(max(prices), 10000, "El precio máximo debe ser menor a 10000")
        self.assertGreater(max(prices), 100, "El precio máximo debe ser mayor a 100")
    
    def test_description_quality(self):
        """Test calidad de las descripciones"""
        for product in self.products:
            description = product["description"]
            self.assertGreater(len(description), 20, f"Descripción muy corta en producto {product.get('product_name', 'Unknown')}")
            self.assertLess(len(description), 500, f"Descripción muy larga en producto {product.get('product_name', 'Unknown')}")
            self.assertIn(product["brand"], description, f"Descripción debe mencionar la marca en producto {product.get('product_name', 'Unknown')}")
    
    def test_ray_ban_products(self):
        """Test productos específicos de Ray-Ban"""
        ray_ban_products = [p for p in self.products if p["brand"] == "Ray-Ban"]
        
        self.assertGreater(len(ray_ban_products), 0, "Debe haber productos de Ray-Ban")
        
        # Verificar modelos específicos
        models = [p["model"] for p in ray_ban_products]
        expected_models = ["Aviator Classic", "Wayfarer Classic", "Clubmaster"]
        
        for model in expected_models:
            self.assertIn(model, models, f"Modelo '{model}' de Ray-Ban no encontrado")
    
    def test_oakley_products(self):
        """Test productos específicos de Oakley"""
        oakley_products = [p for p in self.products if p["brand"] == "Oakley"]
        
        self.assertGreater(len(oakley_products), 0, "Debe haber productos de Oakley")
        
        # Verificar que sean productos deportivos
        for product in oakley_products:
            self.assertIn(product["style"], ["Deportivo", "Wayfarer"], f"Producto Oakley debe ser deportivo: {product.get('product_name', 'Unknown')}")
    
    def test_luxury_brands(self):
        """Test marcas de lujo"""
        luxury_brands = ["Tom Ford", "Gucci", "Prada"]
        
        for brand in luxury_brands:
            brand_products = [p for p in self.products if p["brand"] == brand]
            self.assertGreater(len(brand_products), 0, f"Debe haber productos de {brand}")
            
            # Verificar que sean productos de alta gama
            for product in brand_products:
                self.assertGreater(product["full_price"], 300, f"Producto de {brand} debe ser de alta gama: {product.get('product_name', 'Unknown')}")
    
    def test_catalog_completeness(self):
        """Test completitud del catálogo"""
        # Debe haber al menos 20 productos
        self.assertGreaterEqual(len(self.products), 20, "El catálogo debe tener al menos 20 productos")
        
        # Debe haber al menos 5 marcas diferentes
        brands = set(product["brand"] for product in self.products)
        self.assertGreaterEqual(len(brands), 5, "El catálogo debe tener al menos 5 marcas diferentes")
        
        # Debe haber al menos 3 estilos diferentes
        styles = set(product["style"] for product in self.products)
        self.assertGreaterEqual(len(styles), 3, "El catálogo debe tener al menos 3 estilos diferentes")
        
        # Debe haber al menos 3 colores diferentes
        colors = set(product["color"] for product in self.products)
        self.assertGreaterEqual(len(colors), 3, "El catálogo debe tener al menos 3 colores diferentes")


if __name__ == '__main__':
    unittest.main()

