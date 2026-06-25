from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
import re

ROLES_PERMITIDOS = {"admin", "support", "user"}


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contrasena debe tener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contrasena debe tener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("La contrasena debe tener al menos un numero")
        return v

    @field_validator("role")
    @classmethod
    def validar_role(cls, v: str) -> str:
        if v not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol invalido. Permitidos: {ROLES_PERMITIDOS}")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None