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

model = genai.GenerativeModel("gemini-2.5-pro")

async def correct_text_ai(text_to_correct: str) -> str:
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Correct the following text grammatically and stylistically:\n\n{text_to_correct}")
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Función sincrona por si la necesitas
def correct_text_sync(text_to_correct: str) -> str:
    try:
        chat = model.start_chat()
        chat.send_message(instrucciones)
        response = chat.send_message(f"Correct the following text grammatically and stylistically:\n\n{text_to_correct}")
        return response.text
    except Exception as e:
        return f"Error: {e}"