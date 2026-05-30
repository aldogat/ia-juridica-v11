from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from openai import OpenAI
import os, json

router = APIRouter()

@router.post("/multimodal")
async def multimodal_chat(
    message: str = Form(None),
    messages: str = Form(None),
    consulta: str = Form(None),
    file: UploadFile = File(None)
):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    
    # Extraer el texto de cualquiera de los campos posibles
    msg = message or messages or consulta or ""
    if not msg and file:
        msg = f"[Archivo: {file.filename}]"
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

@router.post("/mensaje")
async def mensaje_chat(message: str = Form(None)):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")
    if not message:
        raise HTTPException(status_code=422, detail="No se encontró 'message' en la solicitud")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}],
            max_tokens=2048
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
