from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import verify_master_key, get_openai_client
from app.schemas.linkedin import LinkedInPostRequest, LinkedInPostResponse
from app.services.linkedin_post import save_linkedin_post

router = APIRouter(dependencies=[Depends(verify_master_key)])

@router.post("/generate-post", response_model=LinkedInPostResponse)
async def generate_linkedin_post(
    payload: LinkedInPostRequest,
    db: Session = Depends(get_db)
):
    """
    Génère un post LinkedIn à partir d’un sujet, ton et audience, puis l’enregistre en base.
    """
    client = get_openai_client()

    prompt = (
        f"Génère un post LinkedIn percutant sur le thème suivant : '{payload.topic}'.\n"
        f"Le ton doit être : {payload.tone}.\n"
        f"Audience ciblée : {payload.audience}.\n"
    )

    if payload.keywords:
        prompt += f"Inclus les mots-clés suivants : {', '.join(payload.keywords)}.\n"

    prompt += "Utilise des emojis, des paragraphes courts et ajoute des hashtags pertinents à la fin."

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en communication LinkedIn."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_post = response.choices[0].message.content.strip()

        save_linkedin_post(
            db=db,
            topic=payload.topic,
            tone=payload.tone,
            audience=payload.audience,
            keywords=payload.keywords,
            content=generated_post
        )

        return LinkedInPostResponse(post=generated_post)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
