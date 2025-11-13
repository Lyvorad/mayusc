import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("CONTRASENA"))

ruta_instrucciones = "instruccionesia.txt"

if not os.path.exists(ruta_instrucciones):
    raise FileNotFoundError(f"File '{ruta_instrucciones}' not found.")

with open(ruta_instrucciones, "r", encoding="utf-8") as f:
    instrucciones = f.read().strip()

if not instrucciones:
    raise ValueError("The file 'instruccionesia.txt' is empty. Please add valid instructions.")

#  Mantener gemini-2.5-pro (Xhale lo necesita)
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,          # Más directo
        max_output_tokens=500,    # Subimos a 500 para evitar truncado
    )
)

#  Versión asincrónica
async def correct_text_ai(text_to_correct: str) -> str:
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Corrige el siguiente texto:\n\n{text_to_correct}")

        # 🔹 Fix: verificar si hay texto antes de acceder
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif response.candidates:
            # Recuperar el texto manualmente
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()
        return "Error: La IA no devolvió texto."
    except Exception as e:
        return f"Error: {e}"

#  Versión sincrónica
def correct_text_sync(text_to_correct: str) -> str:
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Corrige el siguiente texto:\n\n{text_to_correct}")

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()
        return "Error: La IA no devolvió texto."
    except Exception as e:
        return f"Error: {e}"
