import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("CONTRASENA"))

# Leer instrucciones
ruta_instrucciones = "instruccionesia.txt"
if not os.path.exists(ruta_instrucciones):
    raise FileNotFoundError(f"File '{ruta_instrucciones}' not found.")

with open(ruta_instrucciones, "r", encoding="utf-8") as f:
    instrucciones = f.read().strip()

if not instrucciones:
    raise ValueError("The file 'instruccionesia.txt' is empty.")

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,
        max_output_tokens=400,
    )
)

def extraer_texto(response):
    """Evita el error finish_reason=2 devolviendo texto seguro."""
    # Caso 1: tiene texto directo
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    # Caso 2: buscar manualmente en partes
    if response.candidates:
        cand = response.candidates[0]
        if hasattr(cand, "content") and cand.content.parts:
            part = cand.content.parts[0]
            if hasattr(part, "text") and part.text:
                return part.text.strip()

    # Caso 3: no devolvió nada → devolver mensaje seguro
    return "La IA no generó una respuesta. Inténtalo nuevamente."

#  Nueva función estable
def correct_text_sync(text_to_correct: str) -> str:
    try:
        prompt = f"{instrucciones}\n\nCorrige el siguiente texto:\n\n{text_to_correct}"

        response = model.generate_content(prompt)

        return extraer_texto(response)

    except Exception as e:
        return f"Error: {e}"
