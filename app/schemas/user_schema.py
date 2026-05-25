from typing import Literal
from pydantic import BaseModel, EmailStr, Field

roles = Literal['admin', 'support', 'user']
class CrearUsuario(BaseModel):
    name: str = Field(min_lenght=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool