from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field


roles = Literal['admin', 'support', 'user']
class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool

    

class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool

class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
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