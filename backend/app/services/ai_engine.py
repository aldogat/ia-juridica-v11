import openai
import os

def get_openai_client():
    return openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_contract(text: str) -> str:
    client = get_openai_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Analiza el siguiente contrato:\n\n{text}"}],
        max_tokens=1024
    )
    return response.choices[0].message.content

# Agrega aquí cualquier otra función de IA que uses
