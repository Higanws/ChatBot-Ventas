from pydantic import BaseModel, Field


class RasaButton(BaseModel):
    """A button that will be displayed to the user.

    Attributes:

    title: str
        The text that will be displayed on the button

    payload: str
        The payload that will be sent to the chatbot when the button is clicked
    """

    title: str = Field(..., description="The text that will be displayed on the button")
    payload: str = Field(
        ...,
        description="The payload that will be sent to the chatbot when the button is clicked",
    )


class ChatbotResponse(BaseModel):
    """The response from the chatbot.

    Attributes:

    text: str
        The text response from the chatbot

    buttons: List[RasaButton]
        The buttons that will be displayed to the user
    """

    text: str = Field(..., description="The text response from the chatbot")
    buttons: list[RasaButton]


class Product(BaseModel):
    """A sunglasses product that can be recommended to the user.

    Attributes:

    row_id: int
        The ID of the product

    product_name: str
        The name of the product

    brand: str
        The brand of the sunglasses

    model: str
        The model of the sunglasses

    color: str
        The color of the sunglasses

    frame_material: str
        The material of the frame (acetate, metal, titanium, etc.)

    lens_type: str
        The type of lens (polarized, mirrored, gradient, etc.)

    uv_protection: str
        The UV protection level (100% UV400, etc.)

    size: str
        The size of the sunglasses (S, M, L, etc.)

    style: str
        The style of the sunglasses (aviator, wayfarer, sport, etc.)

    full_price: float
        The price of the product

    image_url: str
        URL of the product image

    description: str
        Detailed description of the product

    """

    row_id: int = Field(..., description="The ID of the product")
    product_name: str = Field(..., description="The name of the product")
    brand: str = Field(..., description="The brand of the sunglasses")
    model: str = Field(..., description="The model of the sunglasses")
    color: str = Field(..., description="The color of the sunglasses")
    frame_material: str = Field(..., description="The material of the frame")
    lens_type: str = Field(..., description="The type of lens")
    uv_protection: str = Field(..., description="The UV protection level")
    size: str = Field(..., description="The size of the sunglasses")
    style: str = Field(..., description="The style of the sunglasses")
    full_price: float = Field(..., description="The price of the product")
    image_url: str = Field(..., description="URL of the product image")
    description: str = Field(..., description="Detailed description of the product")
