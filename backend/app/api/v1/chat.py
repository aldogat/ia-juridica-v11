from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os

router = APIRouter()

@router.post("/multimodal")
async def multimodal_chat(data: dict):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    client = OpenAI(api_key=api_key)
    try:
        # Aceptar tanto "messages" (lista) como "message" (string)
        messages = data.get("messages")
        if not messages:
            message_text = data.get("message", "")
            if message_text:
                messages = [{"role": "user", "content": message_text}]
            else:
                raise HTTPException(status_code=422, detail="Se requiere 'message' o 'messages'")
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
