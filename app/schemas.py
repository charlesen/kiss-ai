from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str
    api_key: str | None = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str