from fastapi import APIRouter, Depends
from app.dependencies import verify_master_key, get_openai_client

router = APIRouter(dependencies=[Depends(verify_master_key)])

@router.post("/predict")
async def predict_api():
    """
    Predicts the next message based on the user_message and developer_message inputs.

    - The developer_message is optional and provides additional context for text generation. If this parameter is omitted the OpenAI template will receive only the user_message.

    - The response contains the contents of the generated message.
    """
    pass