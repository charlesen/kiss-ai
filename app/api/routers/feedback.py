from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import verify_master_key

router = APIRouter(dependencies=[Depends(verify_master_key)])

class FeedBack(BaseModel):
    feedback: str
    prediction: str


@router.post("/feedback", response_model=FeedBack, tags=["Feedback"])
async def send_feedback(feedback: FeedBack):
    # Save feedback for model improvement
    return feedback