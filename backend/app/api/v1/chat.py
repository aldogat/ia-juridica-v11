from fastapi import APIRouter, HTTPException, Request
from openai import OpenAI
import os, json

router = APIRouter()

@router.post("/multimodal")
async def multimodal_chat(request: Request):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    
    # Leer el cuerpo crudo y mostrarlo en logs (para que veas qué llega)
    body = await request.body()
    print("Payload recibido:", body.decode())
    try:
        data = json.loads(body)
    except:
        data = {}
    
    # Extraer cualquier campo que contenga un texto
    msg = (
        data.get("message") or
        data.get("messages") or
        data.get("consulta") or
        data.get("query") or
        data.get("prompt") or
        data.get("text") or
        ""
    )
    if isinstance(msg, list):
        # Si es una lista de mensajes, usar el contenido del último
        if msg and isinstance(msg[-1], dict):
            msg = msg[-1].get("content", "")
        else:
            msg = ""
    
    if not msg:
        raise HTTPException(status_code=422, detail=f"No se encontró texto en la solicitud. Campos recibidos: {list(data.keys())}")
    
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}],
            max_tokens=2048
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mensaje")
async def mensaje_chat(request: Request):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    body = await request.body()
    print("Payload recibido en /mensaje:", body.decode())
    try:
        data = json.loads(body)
    except:
        data = {}
    msg = data.get("message") or data.get("text") or ""
    if not msg:
        raise HTTPException(status_code=422, detail="No se encontró 'message' en la solicitud")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}],
            max_tokens=2048
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
