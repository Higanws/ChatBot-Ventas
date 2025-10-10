#!/usr/bin/env python3
"""
Test unitarios para la configuración de Rasa de Óptica Solar
"""

import unittest
import yaml
from pathlib import Path


class TestRasaConfig(unittest.TestCase):
    """Test para la configuración de Rasa"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.config_path = Path("retailGPT/rasa_chatbot/config.yml")
        self.domain_path = Path("retailGPT/rasa_chatbot/domain.yml")
        self.nlu_path = Path("retailGPT/rasa_chatbot/data/nlu.yml")
        
        self.load_configs()
    
    def load_configs(self):
        """Cargar configuraciones"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        with open(self.domain_path, 'r', encoding='utf-8') as f:
            self.domain = yaml.safe_load(f)
        
        with open(self.nlu_path, 'r', encoding='utf-8') as f:
            self.nlu = yaml.safe_load(f)
    
    def test_config_language(self):
        """Test idioma configurado"""
        self.assertEqual(self.config["language"], "es", "El idioma debe ser español")
    
    def test_config_spacy_model(self):
        """Test modelo de Spacy"""
        spacy_nlp = next(component for component in self.config["pipeline"] if component["name"] == "SpacyNLP")
        self.assertEqual(spacy_nlp["model"], "es_core_news_lg", "El modelo de Spacy debe ser para español")
        self.assertFalse(spacy_nlp["case_sensitive"], "El modelo debe ser case insensitive")
    
    def test_config_pipeline_components(self):
        """Test componentes del pipeline"""
        expected_components = [
            "SpacyNLP", "SpacyTokenizer", "SpacyFeaturizer", 
            "DIETClassifier", "RegexFeaturizer", "RegexEntityExtractor",
            "EntitySynonymMapper", "ResponseSelector", "FallbackClassifier"
        ]
        
        actual_components = [component["name"] for component in self.config["pipeline"]]
        
        for component in expected_components:
            self.assertIn(component, actual_components, f"Componente '{component}' no encontrado en el pipeline")
    
    def test_config_diet_classifier(self):
        """Test configuración de DIETClassifier"""
        diet_classifier = next(component for component in self.config["pipeline"] if component["name"] == "DIETClassifier")
        self.assertEqual(diet_classifier["epochs"], 100, "DIETClassifier debe tener 100 epochs")
        self.assertTrue(diet_classifier["constrain_similarities"], "DIETClassifier debe tener constrain_similarities activado")
    
    def test_config_fallback_classifier(self):
        """Test configuración de FallbackClassifier"""
        fallback_classifier = next(component for component in self.config["pipeline"] if component["name"] == "FallbackClassifier")
        self.assertEqual(fallback_classifier["threshold"], 0.8, "FallbackClassifier debe tener threshold 0.8")
        self.assertEqual(fallback_classifier["ambiguity_threshold"], 0.4, "FallbackClassifier debe tener ambiguity_threshold 0.4")
    
    def test_config_policies(self):
        """Test políticas configuradas"""
        self.assertIn("RulePolicy", self.config["policies"], "Debe incluir RulePolicy")
    
    def test_domain_entities(self):
        """Test entidades del dominio"""
        expected_entities = [
            "payment_method", "zipcode", "modify_details",
            "sunglasses_style", "face_shape", "activity_type",
            "brand_preference", "color_preference", "uv_protection"
        ]
        
        for entity in expected_entities:
            self.assertIn(entity, self.domain["entities"], f"Entidad '{entity}' no encontrada en el dominio")
    
    def test_domain_intents(self):
        """Test intents del dominio"""
        expected_intents = [
            "affirm", "bot_challenge", "conversation", "deny", "finish_purchase",
            "goodbye", "greet", "inform", "inform_zipcode", "nlu_fallback",
            "cart_status", "ask_style_recommendation", "ask_face_shape_advice",
            "ask_uv_protection_info", "ask_brand_info", "ask_color_recommendation",
            "ask_activity_sunglasses", "ask_care_instructions"
        ]
        
        for intent in expected_intents:
            self.assertIn(intent, self.domain["intents"], f"Intent '{intent}' no encontrado en el dominio")
    
    def test_domain_actions(self):
        """Test acciones del dominio"""
        expected_actions = [
            "utter_greet", "utter_goodbye", "correct_detail", "llm_processing",
            "process_cached_user_demands", "summarize_details", "validate_zipcode_form",
            "validate_payment_method_form", "validate_confirmation_form",
            "action_default_fallback", "return_cart_status"
        ]
        
        for action in expected_actions:
            self.assertIn(action, self.domain["actions"], f"Acción '{action}' no encontrada en el dominio")
    
    def test_domain_responses_spanish(self):
        """Test respuestas en español"""
        greet_response = self.domain["responses"]["utter_greet"][0]["text"]
        self.assertIn("Óptica Solar", greet_response, "La respuesta de saludo debe mencionar Óptica Solar")
        self.assertIn("gafas de sol", greet_response, "La respuesta de saludo debe mencionar gafas de sol")
        
        goodbye_response = self.domain["responses"]["utter_goodbye"][0]["text"]
        self.assertIn("proteger tus ojos", goodbye_response, "La respuesta de despedida debe mencionar proteger los ojos")
    
    def test_domain_payment_methods(self):
        """Test métodos de pago en el dominio"""
        payment_response = self.domain["responses"]["utter_ask_payment_method"][0]
        self.assertIn("Efectivo", payment_response["text"])
        self.assertIn("Tarjeta de Crédito", payment_response["text"])
        self.assertIn("Tarjeta de Débito", payment_response["text"])
        self.assertIn("MercadoPago", payment_response["text"])
    
    def test_nlu_greet_examples(self):
        """Test ejemplos de saludo en NLU"""
        greet_intent = next(intent for intent in self.nlu["nlu"] if intent["intent"] == "greet")
        examples = greet_intent["examples"]
        
        self.assertIn("hello", examples)
        self.assertIn("hi", examples)
        self.assertIn("good morning", examples)
        self.assertIn("good afternoon", examples)
    
    def test_nlu_sunglasses_intents(self):
        """Test intents específicos de gafas de sol"""
        sunglasses_intents = [
            "ask_style_recommendation", "ask_face_shape_advice", "ask_uv_protection_info",
            "ask_brand_info", "ask_color_recommendation", "ask_activity_sunglasses",
            "ask_care_instructions"
        ]
        
        for intent_name in sunglasses_intents:
            intent = next((intent for intent in self.nlu["nlu"] if intent["intent"] == intent_name), None)
            self.assertIsNotNone(intent, f"Intent '{intent_name}' no encontrado en NLU")
            self.assertGreater(len(intent["examples"]), 0, f"Intent '{intent_name}' debe tener ejemplos")
    
    def test_nlu_conversation_examples(self):
        """Test ejemplos de conversación sobre gafas de sol"""
        conversation_intent = next(intent for intent in self.nlu["nlu"] if intent["intent"] == "conversation")
        examples = conversation_intent["examples"]
        
        # Verificar ejemplos específicos de gafas de sol
        sunglasses_keywords = [
            "sunglasses", "aviator", "wayfarer", "Ray-Ban", "Oakley",
            "polarized", "UV protection", "beach", "running", "driving"
        ]
        
        examples_text = " ".join(examples)
        for keyword in sunglasses_keywords:
            self.assertIn(keyword, examples_text, f"Palabra clave '{keyword}' no encontrada en ejemplos de conversación")
    
    def test_nlu_zipcode_regex(self):
        """Test regex para código postal"""
        zipcode_regex = next(regex for regex in self.nlu["nlu"] if regex["regex"] == "zipcode")
        patterns = zipcode_regex["examples"]
        
        self.assertIn(r"\b[0-9]{5}-[0-9]{3}\b", patterns)
        self.assertIn(r"\b[0-9]{5}[- ]?[0-9]{3}\b", patterns)
        self.assertIn(r"\b[0-9]{8}\b", patterns)
    
    def test_domain_slots_configuration(self):
        """Test configuración de slots"""
        expected_slots = ["zipcode", "legal_age", "payment_method", "modify_details"]
        
        for slot in expected_slots:
            self.assertIn(slot, self.domain["slots"], f"Slot '{slot}' no encontrado en el dominio")
    
    def test_domain_forms_configuration(self):
        """Test configuración de formularios"""
        expected_forms = ["zipcode_form", "payment_method_form", "confirmation_form"]
        
        for form in expected_forms:
            self.assertIn(form, self.domain["forms"], f"Formulario '{form}' no encontrado en el dominio")
    
    def test_domain_session_config(self):
        """Test configuración de sesión"""
        session_config = self.domain["session_config"]
        self.assertEqual(session_config["session_expiration_time"], 60, "Tiempo de expiración de sesión debe ser 60 minutos")
        self.assertTrue(session_config["carry_over_slots_to_new_session"], "Debe llevar slots a nueva sesión")
    
    def test_config_assistant_id(self):
        """Test ID del asistente"""
        self.assertEqual(self.config["assistant_id"], "retailbot", "ID del asistente debe ser 'retailbot'")
    
    def test_config_recipe(self):
        """Test receta de configuración"""
        self.assertEqual(self.config["recipe"], "default.v1", "Receta debe ser 'default.v1'")


if __name__ == '__main__':
    unittest.main()

