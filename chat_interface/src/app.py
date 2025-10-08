import streamlit as st
from chatbot import get_chatbot_response, reset_chatbot_conversation
from PIL import Image
from utils.data_utils import chat_to_word, generate_conversation_id

# Set page title
im = Image.open("./images/neuralmind.png")
st.set_page_config(page_title="Óptica Solar - Asistente Virtual", page_icon=im)

# Hide default Streamlit footer and menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = generate_conversation_id()

# If there are no messages, start new conversation and chatbot
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("🕶️ Óptica Solar - Asistente Virtual")


def process_reset_button_click() -> None:
    """Resets the chatbot conversation."""
    st.session_state.pop("messages", None)
    reset_chatbot_conversation(st.session_state["conversation_id"])


with st.sidebar:
    st.write("¡Bienvenido a Óptica Solar! 🕶️ Tu tienda especializada en gafas de sol de alta calidad.")
    st.button("Reiniciar conversación", on_click=process_reset_button_click)
    st.write(
        "👇 Puedes descargar la conversación actual como documento Word haciendo clic en el botón de abajo."
    )
    conversation_docx = chat_to_word(st.session_state.messages)
    st.download_button(
        "Descargar conversación como archivo Word",
        conversation_docx,
        file_name="historial_conversacion.docx",
    )
    st.header("Instrucciones de Uso")
    st.write(
        "**Lee las instrucciones a continuación para probar mejor el chatbot.**"
    )
    st.write(
        "Envía un mensaje para comenzar una conversación. El chatbot te guiará a través del proceso de compra y puede realizar las siguientes acciones:"
    )
    st.write("- Buscar gafas de sol disponibles")
    st.write("- Proporcionar recomendaciones basadas en tus necesidades")
    st.write("- Agregar y quitar productos de tu carrito")
    st.write("- Finalizar el pedido cuando muestres interés")
    st.write("- Asesorarte sobre protección UV y estilos")
    st.write("Otras acciones no están soportadas en esta versión.")
    st.write(
        "Siéntete libre de enviar mensajes con errores tipográficos, jerga o abreviaciones, simulando un usuario real."
    )
    st.write(
        "Intenta solicitar más de un producto u operación a la vez para explorar el potencial del chatbot."
    )
    st.subheader("Convenciones de Código Postal:")
    st.write(
        "Usaremos tu código postal para simular tu historial de compras. Por lo tanto, considera las siguientes convenciones:"
    )
    st.write(
        "- **Códigos postales que terminan en 0 - 3:** Para cada caso, el usuario tendrá un historial de compras diferente, por lo que el chatbot puede procesar mensajes como 'Quiero lo mismo que ayer'."
    )
    st.write(
        "- **Códigos postales que terminan en 4 - 9:** El usuario no tiene historial de compras."
    )
    st.subheader("Catálogo de Gafas de Sol:")
    st.write(
        "Durante la conversación, se utilizará un catálogo con gafas de sol de marcas premium como Ray-Ban, Oakley, Persol, Tom Ford, Gucci, Prada y Maui Jim."
    )
    st.write(
        "Para propósitos de prueba, algunas de las gafas disponibles en el catálogo son:"
    )
    st.write("- Ray-Ban Aviator Classic Gold")
    st.write("- Oakley Holbrook Matte Black")
    st.write("- Persol 649 Original Marrón")
    st.write("- Tom Ford FT5235 Negro")
    st.write("- Gucci GG0061S Negro")
    st.write(
        "El sistema de recomendación y búsqueda de productos fue desarrollado para esta demostración y no necesariamente refleja el rendimiento de un mecanismo de búsqueda real."
    )


def process_button_click(value, title) -> None:
    """Processes button click and adds the user message to the state."""
    st.session_state.messages.append({"role": "user", "content": title})
    process_message(value)
    # The user message (button reply) and the response are added to the state
    # The button click action refreshes the page, rerunning the display_messages function
    # Therefore, there is no need to call display_messages again here


def display_textual_message(message: dict) -> None:
    """Displays textual messages in the chat window."""

    role = message["role"]
    content = message["content"].replace("\n\n", "\n")

    st.chat_message(role).write(content)


def display_messages(messages=st.session_state.messages) -> None:
    """Displays messages in the chat window."""

    for msg in messages:
        if msg["role"] == "assistant" or msg["role"] == "user":
            display_textual_message(msg)

    # Do not render buttons in the middle of the conversation, only at the end of it:
    if messages and messages[-1]["role"] == "button_pair":
        for button in messages[-1]["content"]:
            title = button["title"]
            value = button["payload"]
            st.button(
                title,
                on_click=lambda value=value, title=title: process_button_click(
                    value, title
                ),
            )


def process_message(user_message: str) -> None:
    """Receives user message and processes it."""
    with st.spinner("Please wait while your message is processed..."):
        bot_responses = get_chatbot_response(
            user_message, st.session_state["conversation_id"]
        )
        for bot_response in bot_responses:
            if "text" in bot_response:
                # Escape $ character to avoid LaTeX rendering:
                content = bot_response["text"].replace("$", "\\$")
                response_dict = {"role": "assistant", "content": content}
                st.session_state.messages.append(response_dict)
            if "buttons" in bot_response:
                # Considering that the buttons come in pairs for positive and negative answers:
                response_dict = {
                    "role": "button_pair",
                    "content": bot_response["buttons"],
                }
                st.session_state.messages.append(response_dict)


display_messages()

if user_message := st.chat_input(placeholder="Escribe tu mensaje aquí... (ej: 'Quiero gafas aviador para la playa')"):
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.chat_message("user").write(user_message)
    process_message(user_message)

    # Rerun the app to display the messages and mount an updated download button
    # Streamlit roadmap plans (in May - July 2024) a feature to mount the
    # download button content dynamically, without the need to rerun the app
    # If such feature is added, we could just display the processed message here and
    # mount the download button dynamically
    st.rerun()

