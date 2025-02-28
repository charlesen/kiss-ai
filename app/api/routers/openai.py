from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.dependencies import verify_master_key, get_openai_client

router = APIRouter(dependencies=[Depends(verify_master_key)])

client = get_openai_client()

class OpenAIResponse(BaseModel):
    content: str

@router.get("/generate", response_model=OpenAIResponse, tags=["OpenAI"])
async def generate_text(
    user_message: str = Query(..., description="Contenu du message pour le rôle user"),
    developer_message: Optional[str] = Query(
        None, description="Contenu du message pour le rôle developer (optionnel)"
    )
):
    messages = []
    if developer_message:
        messages.append({
            "role": "developer",
            "content": developer_message
        })
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        # Appel asynchrone à OpenAI selon la nouvelle interface
        completion = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages
        )
        content = completion.choices[0].message.content
        return OpenAIResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summarize", tags=["OpenAI"])
async def summarize_text(
    text: str = Query(..., description="Texte à résumer")
):
    messages = [
        {"role": "system", "content": "You are a helpful summarizer."},
        {"role": "user", "content": f"Please summarize the following text in the language of the user:\n\n{text}"}
    ]
    try:
        completion = await client.chat.completions.acreate(
            model=settings.openai_model,
            messages=messages
        )
        summary = completion.choices[0].message.content
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

