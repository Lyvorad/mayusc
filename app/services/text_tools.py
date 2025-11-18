from services.ai_connector import correct_text_ai

def to_uppercase(text: str) -> str:
    return text.upper()

def to_lowercase(text: str) -> str:
    return text.lower()

async def correct_with_ai(text: str) -> str:
    return await correct_text_ai(text)
