from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


from app.dependencies import verify_master_key

router = APIRouter(dependencies=[Depends(verify_master_key)])


class SentimentResponse(BaseModel):
    polarity: float
    subjectivity: float


@router.post("/sentiment", response_model=SentimentResponse, tags=["Predict"])
async def analyze_sentiment(
    text: str = Query(..., description="Texte à analyser en anglais")
):
    """
    Analyse le sentiment d'un texte en utilisant TextBlob.

    Renvoie la polarité et la subjectivité du texte.
    - La polarité varie de -1 (négatif) à 1 (positif).
    - La subjectivité varie de 0 (objectif) à 1 (subjectif).
    """
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment
        return SentimentResponse(polarity=sentiment.polarity, subjectivity=sentiment.subjectivity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du sentiment : {str(e)}")

@router.post("/sentiment-fr", response_model=SentimentResponse, tags=["Predict"])
async def analyze_sentiment_fr(
    text: str = Query(..., description="Texte à analyser en français")
):
    """
    Analyse le sentiment d'un texte en français en utilisant TextBlob avec textblob-fr.
    
    - **polarity**: Indique si le sentiment est positif (valeur proche de 1) ou négatif (valeur proche de -1).
    - **subjectivity**: Indique le degré de subjectivité du texte, de 0 (objectif) à 1 (subjectif).
    """
    try:
        # tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

        blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        sentiment = blob.sentiment  # Retourne un tuple (polarity, subjectivity)
        return SentimentResponse(polarity=sentiment[0], subjectivity=sentiment[1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


