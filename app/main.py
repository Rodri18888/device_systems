from fastapi import FastAPI, Request
from app.routes import user_routes

# Crear una instancia de la aplicación FastAPI
app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="2.0.0",
    autor="Rodrigo Velez"
)

# Middleware de cabeceras http
@app.middleware("http")
async def agregar_cabeceras(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response

# Inclusion del router
app.include_router(
    user_routes.router
)

# Definir una ruta básica
@app.get("/",
    summary="Ruta basica",
    description="Ruta basica/principal del sistema",
    response_description="mensaje: Servidor corriendo exitosamente")
def read_root():
    return {"mensaje": "Servidor corriendo exitosamente"}