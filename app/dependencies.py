from fastapi import Header, HTTPException, status
from openai import AsyncOpenAI
from app.config import settings

def verify_master_key(x_master_key: str = Header(...)):
    """
    Vérifie que le header X-Master-Key est présent et correspond 
    à la clé d'authentification master définie dans les paramètres de l'application.
    Si la clé ne correspond pas ou n'est pas présente, 
    une erreur HTTP 401 est levée.
    """
    if x_master_key != settings.master_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé d'authentification invalide."
        )
    return x_master_key

def get_openai_client():
    """
    Renvoie une instance de l'API OpenAI asynchrone initialisée avec la clé d'API définie dans les paramètres de l'application.
    """
    return AsyncOpenAI(api_key=settings.openai_api_key)