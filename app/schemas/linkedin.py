from pydantic import BaseModel
from typing import Optional, List

class LinkedInPostRequest(BaseModel):
    topic: str
    tone: Optional[str] = "Professional"
    audience: Optional[str] = "General"
    keywords: Optional[List[str]] = []

class LinkedInPostResponse(BaseModel):
    post: str
