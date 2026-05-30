from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os

router = APIRouter()

@router.post("/multimodal")
async def multimodal_chat(data: dict):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Si no hay variable, buscar en un header X-API-Key (por si acaso)
        # Pero lo normal es que esté en el entorno
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    client = OpenAI(api_key=api_key)
    try:
        # Acepta "messages" (lista) o "message" (string)
        messages = data.get("messages")
        if not messages:
            msg = data.get("message", "")
            if msg:
                messages = [{"role": "user", "content": msg}]
            else:
                raise HTTPException(status_code=422, detail="Se requiere 'messages' o 'message'")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2048
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mensaje")
async def mensaje_chat(data: dict):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": data.get("message", "")}],
            max_tokens=2048
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
