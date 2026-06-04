from fastapi import FastAPI, HTTPException, Query
from app.data.user_db import user_db
from app.schemas.user_schema import CrearUsuario

app = FastAPI()

def buscar_por_id(user_id: int) -> int:
    user_i = None

    for i, u in enumerate(user_db):
        if u["id"] == user_id:
            user_i = i
            break
    
    if user_i is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user_db[user_i]


