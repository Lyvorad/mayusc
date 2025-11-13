import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

#  Configurar API Key
genai.configure(api_key=os.getenv("CONTRASENA"))

#  Leer instrucciones desde archivo
ruta_instrucciones = "instruccionesia.txt"
if not os.path.exists(ruta_instrucciones):
    raise FileNotFoundError(f"File '{ruta_instrucciones}' not found.")

with open(ruta_instrucciones, "r", encoding="utf-8") as f:
    instrucciones = f.read().strip()

if not instrucciones:
    raise ValueError("The file 'instruccionesia.txt' is empty. Please add valid instructions.")

#  Configurar el modelo Gemini Pro
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,          # más directo
        max_output_tokens=400,    # un poco menos = más rápido
        top_p=0.8,                # reduce variabilidad
        top_k=40
    )
)

#  Función asíncrona (para uso en Flet u otros entornos)
async def correct_text_ai(text_to_correct: str) -> str:
    if not text_to_correct.strip():
        return "Error: No se recibió texto para corregir."
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Corrige el siguiente texto:\n\n{text_to_correct}")

        #  Verificación robusta del contenido
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, "text") and part.text:
                return part.text.strip()
        return "No se recibió respuesta del modelo. Intenta de nuevo."
    except Exception as e:
        return f"Error: {e}"

#  Versión sincrónica (para pruebas locales o scripts simples)
def correct_text_sync(text_to_correct: str) -> str:
    if not text_to_correct.strip():
        return "Error: No se recibió texto para corregir."
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Corrige el siguiente texto:\n\n{text_to_correct}")

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, "text") and part.text:
                return part.text.strip()
        return "No se recibió respuesta del modelo. Intenta de nuevo."
    except Exception as e:
        return f"Error: {e}"
