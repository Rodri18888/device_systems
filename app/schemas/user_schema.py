from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field
from app.data.user_db import user_db

def _init_counter() -> int:
    if not user_db:
        return 0
    return max(user["id"] for user in user_db)

_id_counter = _init_counter()

def get_next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter

roles = Literal['admin', 'support', 'user']
class CrearUsuario(BaseModel):
    id: int = Field(default_factory=get_next_id)
    name: str = Field(min_length=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool

class UsuarioPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[roles] = None  
    is_active: Optional[bool] = None

class UsuarioResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: roles
    is_active: bool = True

    model_config = {"from_attributes": True}    