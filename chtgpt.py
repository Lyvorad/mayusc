import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDdzEN295NvOy0lW_dF5tYzNOGrdueRkpo")

ruta_instrucciones = "instruccionesia.txt"

if not os.path.exists(ruta_instrucciones):
    raise FileNotFoundError(f"No se encontró el archivo '{ruta_instrucciones}'.")

with open(ruta_instrucciones, "r", encoding="utf-8") as f:
    instrucciones = f.read().strip()

if not instrucciones:
    raise ValueError("El archivo 'instruccionesia.txt' está vacío. Por favor, agrega instrucciones válidas.")

model = genai.GenerativeModel("gemini-1.5-flash-latest")

def corregir(texto_a_corregir: str) -> str:
    chat = model.start_chat()
    chat.send_message(instrucciones)
    respuesta = chat.send_message(f"Corrige el siguiente texto:\n\n{texto_a_corregir}")
    return respuesta.text

if __name__ == "__main__":
    texto_prueba = "la jente aveses no save como escribir vien."
    print(corregir(texto_prueba))
