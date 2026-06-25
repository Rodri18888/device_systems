from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field


roles = Literal['admin', 'support', 'user']
class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    hashed_password: str = Field(min_length=8)
    role: roles = Field(default="user")
    is_active: bool

    

class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    hashed_password: str = Field(min_length=8)
    role: roles = Field(default="user")
    is_active: bool

class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    hashed_password: Optional[str]
    role: Optional[roles] = None  
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: roles
    is_active: bool = True

    class Config:
        from_attributes = True    