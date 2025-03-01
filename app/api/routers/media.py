import uuid
import os
from typing import Optional
import pyttsx3
from gtts import gTTS

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from app.dependencies import verify_master_key
router = APIRouter(dependencies=[Depends(verify_master_key)])

class AudioResponse(BaseModel):
    audio_url: str

@router.post("/text-to-speech", response_model=AudioResponse, tags=["Media"])
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

        return AudioResponse(audio_url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion du texte en parole : {str(e)}")
    

@router.post("/text-to-speech-low", response_model=AudioResponse, tags=["Media"])
async def text_to_speech_low(text: str, request: Request, language: Optional[str] = "fr"):
    try:
        # UUID unique pour le nom du fichier
        unique_id = uuid.uuid4()
        # Chemin du fichier audio avec le UUID
        audio_filename = f"{unique_id}.mp3"
        audio_path = os.path.join("public", "medias", audio_filename)

        # Initialisation du moteur pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('voice', language)  # Sélection de la langue
        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        # URL absolue du fichier audio
        # base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")  # Valeur par défaut si la variable n'est pas définie
        # audio_url = f"{base_url}/public/medias/{audio_filename}"
        audio_url = f"{request.base_url}/public/medias/{audio_filename}"

        return AudioResponse(audio_url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion du texte en parole : {str(e)}")