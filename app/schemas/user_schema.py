from typing import Literal
from pydantic import BaseModel, EmailStr, Field

roles = Literal['admin', 'support', 'user']
class CrearUsuario(BaseModel):
    user_id: int = Field(ge=0)
    name: str = Field(min_lenght=3)
    email: EmailStr
    role: roles = Field(default="user")
    is_active: bool