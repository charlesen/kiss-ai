from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.dependencies import verify_master_key, get_openai_client

router = APIRouter(dependencies=[Depends(verify_master_key)])

client = get_openai_client()

class GenerateRequest(BaseModel):
    user_message: str
    developer_message: Optional[str] = Query(
        None, description="Contenu du message pour le rôle developer (optionnel)"
    )

class SummarizeRequest(BaseModel):
    text: str = Query(..., description="Texte à résumer")

class OpenAIResponse(BaseModel):
    content: str

@router.post("/generate", response_model=OpenAIResponse)
async def generate_text(request_data: GenerateRequest
):
    """
    Generates a message based on the user_message and developer_message inputs.
    
    - The developer_message is optional and provides additional context 
    context for text generation. If this parameter is omitted 
    the OpenAI template will receive only the user_message.
    
    - The response contains the contents of the generated message.
    """
    messages = []
    if request_data.developer_message:
        messages.append({
            "role": "developer",
            "content": request_data.developer_message
        })
    messages.append({
        "role": "user",
        "content": request_data.user_message
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

@router.post("/summarize", response_model=OpenAIResponse)
async def summarize_text(request_data: SummarizeRequest):
    """
    Summarizes the given text using an OpenAI model.

    This endpoint receives a text input and generates a summary by interacting
    with the OpenAI API. The summarization is done in the language of the user.

    - Args:
        - text (str): The text to be summarized.

    - Returns:
        - dict: A dictionary containing the summarized text under the key 'summary'.

    - Raises:
        - HTTPException: If an error occurs during the API call, an HTTP 500 error 
        is raised with the error details.
    """

    messages = [
        {"role": "system", "content": "You are a helpful summarizer."},
        {"role": "user", "content": f"Please summarize the following text in the language of the user:\n\n{request_data.text}"}
    ]
    try:
        completion = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages
        )
        summary = completion.choices[0].message.content
        return OpenAIResponse(content=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

