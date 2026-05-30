from typing import Literal
from pydantic import BaseModel, EmailStr, Field

_id_counter = 0

user_db = []

def get_next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter

roles = Literal['admin', 'support', 'user']
class CrearUsuario(BaseModel):
    id: int = Field(default_factory=get_next_id)
    name: str = Field(min_lenght=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool

class UsuarioResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: roles
    is_active: bool = True

    model_config = {"from attributes": True}    