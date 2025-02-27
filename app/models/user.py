from sqlalchemy import Column, Integer, String, Boolean, DateTime
import datetime
from app.core.database import Base  # On importe la Base définie dans database.py

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    api_key = Column(String(32), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
