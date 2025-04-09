from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    bio: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenWithUserResponse(Token, UserResponse):
    pass


class TokenData(BaseModel):
    username: Optional[str] = None
