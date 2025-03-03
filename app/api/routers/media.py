import uuid
import os
from typing import Optional
from gtts import gTTS

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from app.dependencies import verify_master_key
router = APIRouter(dependencies=[Depends(verify_master_key)])

class MediaResponse(BaseModel):
    audio_url: str

@router.post("/text-to-speech", response_model=MediaResponse)
async def text_to_speech(text: str, request: Request, language: Optional[str] = "fr"):
    try:
        # Initialisation du moteur gtts        
        tts = gTTS(text, lang=language, slow=False)
        # Chemin du fichier audio avec le UUID
        # UUID unique pour le nom du fichier
        unique_id = uuid.uuid4()
        audio_filename = f"{unique_id}.mp3"
        audio_path = os.path.join("public", "medias", audio_filename)
        
        tts.save(audio_path)

        # URL absolue du fichier audio
        audio_url = f"{request.base_url}/public/medias/{audio_filename}"

        return MediaResponse(audio_url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion du texte en parole : {str(e)}")
    

