from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import edge_tts
import asyncio
import tempfile
import os
import uuid

app = FastAPI()

VOICE = "pt-BR-AntonioNeural"

async def gerar_audio(texto: str, caminho_saida: str):
    communicate = edge_tts.Communicate(texto=texto, voice=VOICE)
    await communicate.save(caminho_saida)

@app.get("/")
def raiz():
    return {"ok": True, "servico": "tts", "voice": VOICE}

@app.get("/tts")
async def tts(texto: str = Query(..., min_length=1, max_length=500)):
    try:
        nome_arquivo = f"tts_{uuid.uuid4().hex}.mp3"
        caminho = os.path.join(tempfile.gettempdir(), nome_arquivo)

        await gerar_audio(texto, caminho)

        if not os.path.exists(caminho):
            raise HTTPException(status_code=500, detail="Áudio não gerado")

        return FileResponse(
            path=caminho,
            media_type="audio/mpeg",
            filename="audio.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))