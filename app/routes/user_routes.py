from fastapi import APIRouter, status, Depends, Body
from app.schemas.user_schema import CrearUsuario, UsuarioPatch, UsuarioResponse, get_next_id
from app.data.user_db import user_db
from app.dependencies.user_dependencies import buscar_por_id
from typing import Optional

router = APIRouter()

# Rutas GET

##GET /users

@router.get("/users/", tags=["Users"],
    summary="Obtener todos los usuarios",
    description="Obtiene cada usuario del sistema con su informacion",
    response_description="Usuarios obtenidos con exito",
    response_model=list[UsuarioResponse])
async def obtener_usuarios(role: Optional[str] = None, is_active: Optional[bool] = None):
    
    if role:
        users = [user for user in user_db if user["id"] == role]
        return users
    
    if is_active is not None:
        users = [user for user in user_db if user["is_active"] == is_active]
        return users
    
    return user_db

##GET /users/{user_id}

@router.get("/users/{user_id}", tags=["Users"],
    summary="Obtener un usuario por id",
    description="Obtiene un usuario segun la id indicada en la ruta",
    response_description="Usuario obtenido con exito", 
    response_model=UsuarioResponse)
async def obtener_usuario(user:  dict = Depends(buscar_por_id)):
    return user


# Rutas POST

##POST /users

@router.post("/users/", tags=["Users"],
    summary="Enviar un usuario al sistema",
    description="Envia un usuario con los datos indicados",
    response_description="Usuario enviado con exito", 
    status_code=status.HTTP_201_CREATED, response_model=UsuarioResponse)
async def crear_usuario(user: CrearUsuario):
    nuevo = {"id": get_next_id(), **user.model_dump()}
    user_db.append(nuevo)
    return nuevo


# Rutas PUT y PATCH

##PUT /users/{user_id}

@router.put("/users/{user_id}", tags=["Users"],
    summary="Actualizar un usuario",
    description="Actualiza todos los datos de un usuario",
    response_description="Usuario actualizado con exito", 
    response_model=UsuarioResponse)
async def actualizar_usuario_put(user: CrearUsuario, user_id: int, user_actual: dict = Depends(buscar_por_id)):
        
    
    new_user = {"id": user_id, "name": user.name, "email": user.email, "role": user.role, "is_active": user.is_active}

    user_i = None
    for i, u in enumerate(user_db):
        if u["id"] == user_id:
            user_i = i
            break

    user_db[user_i] = new_user

    return new_user


##PATCH /users/{user_id}

@router.patch("/users/{user_id}", tags=["Users"],
    summary="Actualizar un usuario",
    description="Actualiza uno o mas datos de un usuario",
    response_description="Usuarios actualizado con exito", 
    response_model=UsuarioResponse)
async def actualizar_usuario_patch(user_id: int, user: UsuarioPatch = Body(...), user_actual: dict = Depends(buscar_por_id)):
    
    datos_actualizacion = user.model_dump(exclude_unset=True)

    
    for campo, valor in datos_actualizacion.items():
        user_actual[campo] = valor


    return user_actual  



# Rutas DELETE

##DELETE /users/{user_id}
    
@router.delete("/users/{user_id}", tags=["Users"],
    summary="Eliminar un usuario",
    description="Elimina un usuario del sistema segun la id indicada",
    response_description="Usuario eliminado con exito", 
    response_model=UsuarioResponse)
async def obtener_usuario(user_id: int, user_i: dict = Depends(buscar_por_id)):
    user_i = None
    for i, u in enumerate(user_db):
        if u["id"] == user_id:
            user_i = i
            break

    usuario_eliminado = user_db.pop(user_i)

    return usuario_eliminado    