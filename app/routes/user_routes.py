from fastapi import APIRouter
from app.schemas.user_schema import CrearUsuario, user_db

router = APIRouter()

# Rutas GET

##GET /users

@router.get("/users/")
async def obtener_usuarios():
    return user_db

##GET /users/{user_id}



##GET /users?role=admin



##GET /users?is_active=true





# Rutas POST

##POST /users

@router.post("/users/")
async def crear_usuario(user: CrearUsuario):
    user_db.append(user)
    return {"mensaje": f"Usuario {user.name} fue creado con exito"}
