from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import verify_master_key, get_openai_client
from app.schemas.linkedin import LinkedInPostRequest, LinkedInPostResponse
from app.models.linkedin_post import LinkedInPost
from openai import AsyncOpenAI
from typing import Dict

router = APIRouter(dependencies=[Depends(verify_master_key)])
client: AsyncOpenAI = get_openai_client()

# Prompts templates par style
PROMPT_TEMPLATES: Dict[str, str] = {
    "inspiration": (
        "Tu es un expert LinkedIn qui aide les freelances et créateurs à publier des posts inspirants.\n"
        "Génère un post court (3 à 5 lignes) sur le thème suivant : \"{topic}\".\n"
        "Le post doit inclure :\n"
        "- une émotion ou une leçon personnelle\n"
        "- une tournure motivante ou engageante\n"
        "- une phrase de clôture qui invite à réfléchir\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}\n"
        "Style : LinkedIn natif, sans hashtags"
    ),
    "storytelling": (
        "Tu es un coach LinkedIn. Aide-moi à transformer une anecdote simple en post puissant.\n"
        "Voici mon anecdote : \"{topic}\"\n"
        "Structure le post en :\n"
        "- Contexte (accroche)\n"
        "- Problème / moment clé\n"
        "- Résolution ou apprentissage\n"
        "- Appel à réflexion ou à engagement\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}\n"
        "Style : Narratif, fluide, sans hashtags"
    ),
    "cta": (
        "Génère un post professionnel avec un appel à l’action clair pour inciter à : {topic}\n"
        "Le post doit :\n"
        "- Attirer l’attention dès la 1ère ligne\n"
        "- Expliquer en quoi cela aide la cible\n"
        "- Finir par un CTA simple (ex: \"Dispo en DM\", \"Contactez-moi\", etc.)\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}\n"
        "Style : Concis, orienté résultat"
    ),
    "thread": (
        "Crée un thread LinkedIn éducatif en 5 points maximum.\n"
        "Sujet : \"{topic}\"\n"
        "Chaque point doit être clair, utile et compréhensible pour les non-experts.\n"
        "Ajoute une accroche forte au début et une conclusion qui donne envie de liker/commenter.\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}\n"
        "Style : format thread (avec \"1.\", \"2.\", ...)"
    ),
    "stat_opinion": (
        "Crée un post autour de cette statistique : \"{topic}\"\n"
        "Objectif : choquer, éveiller ou faire réagir.\n"
        "Structure :\n"
        "- Stat choc\n"
        "- Explication ou mise en contexte\n"
        "- Opinion ou interprétation personnelle\n"
        "- Question engageante pour finir\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}"
    ),
    "service_announcement": (
        "Tu es un consultant qui veut annoncer une nouvelle offre de service.\n"
        "Sujet : \"{topic}\"\n"
        "Le post doit :\n"
        "- Ne pas sonner comme une pub\n"
        "- Apporter de la valeur avant de vendre\n"
        "- Inclure une phrase naturelle pour proposer de discuter\n\n"
        "Langue : {language}\n"
        "Tonalité : {tone}"
    ),
}


@router.post("/generate-post", response_model=LinkedInPostResponse)
async def generate_linkedin_post(
    request: LinkedInPostRequest,
    db: Session = Depends(get_db),
):
    # Générer le prompt basé sur le style demandé
    style = request.prompt_style.lower()
    if style not in PROMPT_TEMPLATES:
        raise HTTPException(status_code=400, detail="Invalid prompt_style")

    prompt_template = PROMPT_TEMPLATES[style]
    prompt = prompt_template.format(
        topic=request.topic,
        tone=request.tone,
        audience=request.audience,
        language=request.language,
    )

    # Appel à OpenAI
    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert de la rédaction LinkedIn."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Enregistrer le post en BDD
    post = LinkedInPost(
        topic=request.topic,
        tone=request.tone,
        audience=request.audience,
        keywords=", ".join(request.keywords) if request.keywords else "",
        content=content
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    return LinkedInPostResponse(post=content)
