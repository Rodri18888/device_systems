from fastapi import APIRouter
from app.schemas.user_schema import CrearUsuario, user_db
from typing import Optional

router = APIRouter()

# Rutas GET

##GET /users

@router.get("/users/")
async def obtener_usuarios(role: Optional[str] = None, is_active: Optional[bool] = None):
    
    if role:
        users = [user for user in user_db if user.role == role]
        return {"users": users}
    
    if is_active is not None:
        users = [user for user in user_db if user.is_active == is_active]
        return {"users": users}
    
    return {"users": user_db}

##GET /users/{user_id}

@router.get("/users/{user_id}")
async def obtener_usuario(user_id: int):
    for user in user_db:
        if user.id == user_id:
            return user 


# Rutas POST

##POST /users

@router.post("/users/")
async def crear_usuario(user: CrearUsuario):
    user_db.append(user)
    return {"mensaje": f"Usuario {user.name} fue creado con exito"}
