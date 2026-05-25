from fastapi import APIRouter
from app.schemas import CrearUsuario

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Rutas GET

##GET /users

@router.get("/")
def obtener_usuarios():
    return

##GET /users/{user_id}



##GET /users?role=admin



##GET /users?is_active=true





# Rutas POST

##POST /users

@router.post("/")
def crear_usuario(user: CrearUsuario):
    return {"mensaje": f"Usuario {user.name} fue creado con exito"}
