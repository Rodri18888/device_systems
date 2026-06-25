from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re

roles = Literal["admin", "support", "user"]


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    role: roles = Field(default="user")
    is_active: bool = True

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe tener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe tener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe tener al menos un numero")
        return v


class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    role: roles = Field(default="user")
    is_active: bool

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe tener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe tener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe tener al menos un numero")
        return v


class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[roles] = None
    is_active: Optional[bool] = None

    @field_validator("password", mode="before")
    @classmethod
    def validar_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe tener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe tener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe tener al menos un numero")
        return v


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: roles
    is_active: bool

    model_config = ConfigDict(from_attributes=True)