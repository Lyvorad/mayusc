import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()
genai.configure(api_key=os.getenv("CONTRASENA"))

# Ruta del archivo de instrucciones
ruta_instrucciones = "instruccionesia.txt"

# Leer las instrucciones
if not os.path.exists(ruta_instrucciones):
    raise FileNotFoundError(f"File '{ruta_instrucciones}' not found.")

with open(ruta_instrucciones, "r", encoding="utf-8") as f:
    instrucciones = f.read().strip()

if not instrucciones:
    raise ValueError("The file 'instruccionesia.txt' is empty. Please add valid instructions.")

# Modelo: seguimos usando gemini-2.5-pro por compatibilidad con Xhale
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,          # Menos divagación → más rapidez y coherencia
        max_output_tokens=300     # Limita la salida a lo necesario
    )
)

#  Versión asincrónica optimizada
async def correct_text_ai(text_to_correct: str) -> str:
    try:
        prompt = f"{instrucciones}\n\nTexto a corregir:\n{text_to_correct}"
        # Ejecutar en hilo separado para no bloquear el evento loop
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

#  Versión sincrónica (por compatibilidad con Flet)
def correct_text_sync(text_to_correct: str) -> str:
    try:
        prompt = f"{instrucciones}\n\nTexto a corregir:\n{text_to_correct}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
