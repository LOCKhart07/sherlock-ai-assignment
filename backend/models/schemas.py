from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    bio: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
