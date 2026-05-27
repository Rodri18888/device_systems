from fastapi import FastAPI
from app.routes import user_routes

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Inclusion del router
app.include_router(
    user_routes.router
)

# Definir una ruta básica
@app.get("/")
def read_root():
    return {"mensaje": "Servidor corriendo exitosamente"}