from fastapi import APIRouter, status, Depends, Response, HTTPException
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate, DeviceResponse
from sqlalchemy.orm import Session
from app.services.device_service import *
from app.dependencies.database_dependencies import get_db
from app.database.connection import engine, Base
from typing import List

Base.metadata.create_all(bind=engine)

router = APIRouter()

# Rutas GET

##GET /devices

@router.get("/devices/", tags=["Devices"],
    summary="Obtener todos los dispositivos",
    description="Obtiene cada dispositivo del sistema con su informacion",
    response_description="Dispositivos obtenidos con exito",
    response_model=list[DeviceResponse])
async def obtener_dispositivos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
     devices = obtener_dispositivos(db, skip=skip, limit=limit)
     return devices
    
    

##GET /devices/{dispositivo_id}

@router.get("/devices/{dispositivo_id}", tags=["Devices"],
    summary="Obtener un dispositivo por id",
    description="Obtiene un dispositivo segun la id indicada en la ruta",
    response_description="Dispositivo obtenido con exito",
    response_model=DeviceResponse)
async def obtener_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(get_db)):
    db_dispositivo = obtener_dispositivo_id(db=db, dispositivo_id=dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db_dispositivo


# Rutas POST

##POST /devices/

@router.post("/devices/", tags=["Devices"],
    summary="Crear un dispositivo",
    description="Registra un dispositivo con los datos indicados",
    response_description="Dispositivo creado con exito",
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceResponse)
async def crear_dispositivo_endpoint(device: DeviceCreate, db: Session = Depends(get_db)):
    serial_existente = db.query(Device).filter(Device.serial_number == device.serial_number).first()
    if serial_existente:
        raise HTTPException(status_code=400, detail="Numero de serie duplicado")
    return crear_dispositivo(db=db, device_data=device)


# Rutas PUT y PATCH

##PUT /devices/{dispositivo_id}

@router.put("/devices/{dispositivo_id}", tags=["Devices"],
    summary="Actualizar un dispositivo completo",
    description="Reemplaza todos los datos de un dispositivo",
    response_description="Dispositivo actualizado con exito",
    response_model=DeviceResponse)
async def actualizar_dispositivo_endpoint(
    dispositivo_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    db_dispositivo = actualizar_dispositivo(db=db, dispositivo_id=dispositivo_id, device_data=device)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db_dispositivo


##PATCH /devices/{dispositivo_id}

@router.patch("/devices/{dispositivo_id}", tags=["Devices"],
    summary="Actualizar un dispositivo parcialmente",
    description="Actualiza uno o mas campos de un dispositivo",
    response_description="Dispositivo actualizado con exito",
    response_model=DeviceResponse)
async def actualizar_dispositivo_parcial_endpoint(
    dispositivo_id: int,
    device: DevicePatch,
    db: Session = Depends(get_db)
):
    db_dispositivo = obtener_dispositivo_id(db=db, dispositivo_id=dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return actualizar_dispositivo_parcial(db=db, dispositivo_id=dispositivo_id, device_data=device)


# Rutas DELETE

##DELETE /devices/{dispositivo_id}

@router.delete("/devices/{dispositivo_id}", tags=["Devices"],
    summary="Eliminar un dispositivo",
    description="Elimina un dispositivo del sistema segun la id indicada",
    response_description="Dispositivo eliminado con exito",
    status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_dispositivo(db=db, dispositivo_id=dispositivo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)