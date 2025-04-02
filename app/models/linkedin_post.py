from sqlalchemy import Column, Integer, String, Text, DateTime, func
# from sqlalchemy.sql import func
from app.db import Base  # Utilise la base SQLAlchemy déclarée dans app.db

class LinkedInPost(Base):
    __tablename__ = "linkedin_posts"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    tone = Column(String(100), nullable=True)
    audience = Column(String(100), nullable=True)
    keywords = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"LinkedInPost(id={self.id}, topic={self.topic}, tone={self.tone}, audience={self.audience}, keywords={self.keywords}, content={self.content})"