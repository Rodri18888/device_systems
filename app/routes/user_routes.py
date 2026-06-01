from fastapi import APIRouter
from app.schemas.user_schema import CrearUsuario, UsuarioResponse, get_next_id
from app.data.user_db import user_db
from typing import Optional

router = APIRouter()

# Rutas GET

##GET /users

@router.get("/users/", response_model=list[UsuarioResponse])
async def obtener_usuarios(role: Optional[str] = None, is_active: Optional[bool] = None):
    
    if role:
        users = [user for user in user_db if user["id"] == role]
        return users
    
    if is_active is not None:
        users = [user for user in user_db if user["is_active"] == is_active]
        return users
    
    return user_db

##GET /users/{user_id}

@router.get("/users/{user_id}", response_model=UsuarioResponse)
async def obtener_usuario(user_id: int):
    for user in user_db:
        if user["id"] == user_id:
            return user 


# Rutas POST

##POST /users

@router.post("/users/", response_model=UsuarioResponse)
async def crear_usuario(user: CrearUsuario):
    nuevo = {"id": get_next_id(), **user.model_dump()}
    user_db.append(nuevo)
    return nuevo


# Rutas PUT y PATCH

##PUT /users/{user_id}

@router.put("/users/{user_id}", response_model=UsuarioResponse)
async def actualizar_usuario_put(user_id: int, user: CrearUsuario):
    user_i = None

    for i, u in enumerate(user_db):
        if u["id"] == user_id:
            user_i = i
            
    
    new_user = {"id": user_id, "name": user.name, "email": user.email, "role": user.role, "is_active": user.is_active}

    user_db[user_i] = new_user

    return new_user


##PATCH /users/{user_id}

@router.patch("/users/{user_id}", response_model=UsuarioResponse)
async def actualizar_usuario_patch(user_id: int, user: CrearUsuario):
    