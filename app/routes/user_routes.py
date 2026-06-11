from fastapi import APIRouter, status, Depends, Body, Response
from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate, get_next_id
from sqlalchemy.orm import Session
from app.services.user_service import *
from app.dependencies.database_dependencies import get_db
from app.database.connection import engine, Base

Base.metadata.create_all(bind=engine)

router = APIRouter()

# Rutas GET

##GET /users

@router.get("/users/", tags=["Users"],
    summary="Obtener todos los usuarios",
    description="Obtiene cada usuario del sistema con su informacion",
    response_description="Usuarios obtenidos con exito",
    response_model=list[UserResponse])
async def obtener_usuarios_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
     users = obtener_usuarios(db, skip=skip, limit=limit)
     return users
    
    

##GET /users/{user_id}

@router.get("/users/{usuario_id}", tags=["Users"],
    summary="Obtener un usuario por id",
    description="Obtiene un usuario segun la id indicada en la ruta",
    response_description="Usuario obtenido con exito", 
    response_model=UserResponse)
async def obtener_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = obtener_usuario_id(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
    


# Rutas POST

##POST /users

@router.post("/users/", tags=["Users"],
    summary="Enviar un usuario al sistema",
    description="Envia un usuario con los datos indicados",
    response_description="Usuario enviado con exito", 
    status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def crear_usuario_endpoint(usuario: UserCreate, db: Session = Depends(get_db)):
     return crear_usuario(db=db, usuario_data=usuario)


# Rutas PUT y PATCH

##PUT /users/{user_id}

@router.put("/users/{usuario_id}", tags=["Users"],
    summary="Actualizar un usuario",
    description="Actualiza todos los datos de un usuario",
    response_description="Usuario actualizado con exito", 
    response_model=UserResponse)
async def actualizar_usuario_endpoint(
    usuario_id: int,
    usuario: UserUpdate,
    db: Session = Depends(get_db)
):
    db_usuario = actualizar_usuario(db=db, usuario_id=usuario_id, usuario_data=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario



##PATCH /users/{user_id}

@router.patch("/users/{usuario_id}", tags=["Users"],
    summary="Actualizar un usuario",
    description="Actualiza uno o mas datos de un usuario",
    response_description="Usuarios actualizado con exito", 
    response_model=UserResponse)
async def actualizar_usuario_endpoint(
    usuario_id: int,
    usuario: UserPatch,
    db: Session = Depends(get_db)
):
    db_usuario = actualizar_usuario_parcial(db=db, usuario_id=usuario_id, usuario_data=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


# Rutas DELETE

##DELETE /users/{user_id}
    
@router.delete("/users/{usuario_id}", tags=["Users"],
    summary="Eliminar un usuario",
    description="Elimina un usuario del sistema segun la id indicada",
    response_description="Usuario eliminado con exito", 
    status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_usuario(db=db, usuario_id=usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)    