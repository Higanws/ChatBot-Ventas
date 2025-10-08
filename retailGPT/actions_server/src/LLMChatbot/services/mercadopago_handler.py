import os
import json
from typing import Dict, Any, Optional
import requests
from .cart_handler import CartHandler


class MercadoPagoHandler:
    """Handles MercadoPago payment processing for sunglasses orders."""

    def __init__(self):
        self.access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
        self.base_url = "https://api.mercadopago.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def create_payment_preference(self, user_id: str, cart: list, zipcode: str) -> Dict[str, Any]:
        """
        Creates a MercadoPago payment preference for the user's cart.

        Args:
            user_id: The user's ID
            cart: The user's shopping cart
            zipcode: The user's ZIP code

        Returns:
            Dictionary containing payment preference data
        """
        if not self.access_token:
            return {
                "error": "MercadoPago access token not configured",
                "success": False
            }

        try:
            # Calculate total amount
            total_amount = self._calculate_total_amount(cart)
            
            # Create items for MercadoPago
            items = self._create_items_from_cart(cart)
            
            # Create payment preference
            preference_data = {
                "items": items,
                "payer": {
                    "name": "Cliente",
                    "email": f"cliente_{user_id}@opticasolar.com"
                },
                "back_urls": {
                    "success": "https://opticasolar.com/success",
                    "failure": "https://opticasolar.com/failure",
                    "pending": "https://opticasolar.com/pending"
                },
                "auto_return": "approved",
                "external_reference": f"opticasolar_{user_id}",
                "notification_url": "https://opticasolar.com/webhooks/mercadopago",
                "metadata": {
                    "user_id": user_id,
                    "zipcode": zipcode,
                    "store": "opticasolar"
                }
            }

            # Make API call to MercadoPago
            response = requests.post(
                f"{self.base_url}/checkout/preferences",
                headers=self.headers,
                json=preference_data
            )

            if response.status_code == 201:
                preference = response.json()
                return {
                    "success": True,
                    "preference_id": preference["id"],
                    "init_point": preference["init_point"],
                    "sandbox_init_point": preference.get("sandbox_init_point"),
                    "total_amount": total_amount
                }
            else:
                return {
                    "error": f"MercadoPago API error: {response.status_code}",
                    "success": False
                }

        except Exception as e:
            return {
                "error": f"Error creating payment preference: {str(e)}",
                "success": False
            }

    def _calculate_total_amount(self, cart: list) -> float:
        """Calculate total amount from cart items."""
        total = 0.0
        for item in cart:
            total += item["price_per_unit"] * item["number_of_units"]
        return round(total, 2)

    def _create_items_from_cart(self, cart: list) -> list:
        """Create MercadoPago items from cart."""
        items = []
        for item in cart:
            items.append({
                "title": item["product_name"],
                "quantity": item["number_of_units"],
                "unit_price": item["price_per_unit"],
                "currency_id": "ARS"  # Argentine Peso
            })
        return items

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status from MercadoPago.

        Args:
            payment_id: The payment ID from MercadoPago

        Returns:
            Dictionary containing payment status
        """
        if not self.access_token:
            return {
                "error": "MercadoPago access token not configured",
                "success": False
            }

        try:
            response = requests.get(
                f"{self.base_url}/v1/payments/{payment_id}",
                headers=self.headers
            )

            if response.status_code == 200:
                payment = response.json()
                return {
                    "success": True,
                    "status": payment["status"],
                    "status_detail": payment["status_detail"],
                    "transaction_amount": payment["transaction_amount"],
                    "currency_id": payment["currency_id"]
                }
            else:
                return {
                    "error": f"Error getting payment status: {response.status_code}",
                    "success": False
                }

        except Exception as e:
            return {
                "error": f"Error getting payment status: {str(e)}",
                "success": False
            }

    def process_payment_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process MercadoPago webhook notification.

        Args:
            webhook_data: Webhook data from MercadoPago

        Returns:
            Dictionary containing processing result
        """
        try:
            # Extract payment information from webhook
            payment_id = webhook_data.get("data", {}).get("id")
            
            if not payment_id:
                return {
                    "error": "No payment ID in webhook data",
                    "success": False
                }

            # Get payment status
            payment_status = self.get_payment_status(payment_id)
            
            if payment_status["success"]:
                status = payment_status["status"]
                
                if status == "approved":
                    # Payment approved - process order
                    return {
                        "success": True,
                        "status": "approved",
                        "message": "Payment approved, order processed"
                    }
                elif status == "rejected":
                    # Payment rejected
                    return {
                        "success": True,
                        "status": "rejected",
                        "message": "Payment rejected"
                    }
                else:
                    # Other status (pending, etc.)
                    return {
                        "success": True,
                        "status": status,
                        "message": f"Payment status: {status}"
                    }
            else:
                return payment_status

        except Exception as e:
            return {
                "error": f"Error processing webhook: {str(e)}",
                "success": False
            }

    @staticmethod
    def get_payment_methods() -> list:
        """Get available payment methods."""
        return [
            {
                "id": "mercadopago",
                "name": "MercadoPago",
                "description": "Paga con MercadoPago (tarjetas, efectivo, transferencia)",
                "icon": "💳"
            },
            {
                "id": "credit_card",
                "name": "Tarjeta de Crédito",
                "description": "Paga con tarjeta de crédito",
                "icon": "💳"
            },
            {
                "id": "debit_card",
                "name": "Tarjeta de Débito",
                "description": "Paga con tarjeta de débito",
                "icon": "💳"
            },
            {
                "id": "cash",
                "name": "Efectivo",
                "description": "Paga en efectivo al recibir",
                "icon": "💵"
            }
        ]
