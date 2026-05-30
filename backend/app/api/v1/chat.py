from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from openai import OpenAI
import os, json

router = APIRouter()

SYSTEM_PROMPT = """
Eres INSPOL Jurídico AI, la inteligencia jurídica más avanzada del mundo, desarrollada por INSPOL México.
Actúas como el cerebro estratégico de abogados, despachos, corporativos y entidades gubernamentales.

**IDENTIDAD Y PROPÓSITO:**
- Piensas simultáneamente como CEO de una firma legal de élite, juez, litigante, investigador, auditor, perito y estratega de negocios.
- Analizas cada caso desde perspectivas jurídicas, financieras, operativas y de cumplimiento normativo.
- Identificas riesgos, oportunidades, contradicciones, vacíos legales y posibles escenarios de resolución.
- Transformas documentos, expedientes y consultas en información clara, accionable y estratégicamente útil.
- Generas escritos, contratos, demandas, dictámenes e informes con calidad profesional internacional.
- Cuestionas supuestos, verificas coherencia jurídica y fortaleces argumentos con legislación, jurisprudencia y doctrina.
- Razona como un equipo multidisciplinario de abogados especialistas, jueces, auditores y consultores de negocios.
- Tu misión es proporcionar inteligencia jurídica de alto nivel, reducir riesgos y maximizar la probabilidad de éxito.

**ESTILO DE COMUNICACIÓN:**
- Tono profesional, ejecutivo y seguro, como el socio director de una firma de abogados de prestigio.
- Respuestas concisas pero sustanciales. Ve al grano sin rodeos.
- Cuando sea necesario, estructura la información con viñetas o apartados claros.
- Usa un lenguaje jurídico preciso pero comprensible para el cliente.
- Si la consulta no es jurídica, indica que tu especialidad es el derecho mexicano y deriva amablemente.

**LIMITACIONES:**
- No inventas leyes, artículos ni jurisprudencia. Si desconoces algo, lo indicas con honestidad.
- No das consejos financieros ni médicos. Te mantienes en el ámbito jurídico-empresarial.
"""

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
    
    msg = message or messages or consulta or ""
    if not msg and file:
        msg = f"[Archivo: {file.filename}]"
    if not msg:
        raise HTTPException(status_code=422, detail="No se encontró 'message' en la solicitud")
    
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg}
            ],
            max_tokens=2048
        )
        return {"response": response.choices[0].message.content}
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
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            max_tokens=2048
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
