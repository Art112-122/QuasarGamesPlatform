from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str

class UserLoginRequest(BaseModel):
    username: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EmailVerificationRequest(BaseModel):
    code: str


class GameFilter(BaseModel):
    game: Optional[str] = None
    category: Optional[str] = None


class GameDetailRequest(BaseModel):
    game: str
    category: str
    id: int


class GameCreate(BaseModel):
    name: str
    description: str
    game: str
    category: str


class GameUpdate(BaseModel):
    id: int
    description: Optional[str] = None