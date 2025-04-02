from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class LinkedInPostRequest(BaseModel):
    topic: str = Field(..., description="Sujet principal du post à générer.")
    tone: Optional[str] = Field("Professional", description="Tonalité du post (ex: professionnel, motivant, amical)")
    audience: Optional[str] = Field("General", description="Cible du post (ex: développeurs, entrepreneurs, freelances)")
    prompt_style: Optional[Literal[
        "inspiration",
        "storytelling",
        "cta",
        "thread",
        "stat_opinion",
        "service_announcement"
    ]] = Field("inspiration", description="Style de prompt à utiliser pour structurer le post")
    language: Optional[Literal["English", "French"]] = Field("English", description="Langue dans laquelle générer le post")
    keywords: Optional[List[str]] = Field(default_factory=list, description="Liste optionnelle de mots-clés à inclure")

class LinkedInPostResponse(BaseModel):
    post: str = Field(..., description="Contenu généré du post LinkedIn")
