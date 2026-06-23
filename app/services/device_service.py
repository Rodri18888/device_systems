from sqlalchemy.orm import Session
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate, DeviceResponse


##Crear dispositivo.

def crear_dispositivo(db: Session, device_data: DeviceCreate):

    db_device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand,
        is_available=device_data.is_available
    )

    db.add(db_device)

    db.commit()

    db.refresh(db_device)

    return db_device


##Listar dispositivos.

def obtener_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Device).offset(skip).limit(limit).all()


##Buscar dispositivo por ID.

def obtener_dispositivo_id(db: Session, dispositivo_id: int):
    return db.query(Device).filter(Device.id == dispositivo_id).first()


##Actualizar dispositivo completo.

def actualizar_dispositivo(db: Session, dispositivo_id: int, device_data: DeviceUpdate):
    
    db_dispositivo = db.query(Device).filter(Device.id == dispositivo_id).first()

    if db_dispositivo:
        db_dispositivo.name = device_data.name
        db_dispositivo.serial_number = device_data.serial_number
        db_dispositivo.device_type = device_data.device_type
        db_dispositivo.brand = device_data.brand
        db_dispositivo.is_available = device_data.is_available
        

        # Confirmar cambios
        db.commit()
        db.refresh(db_dispositivo)

    return db_dispositivo


##Actualizar dispositivo parcial.

def actualizar_dispositivo_parcial(db: Session, dispositivo_id: int, device_data: DevicePatch):

    db_dispositivo = db.query(Device).filter(Device.id == dispositivo_id).first()
    update_data = device_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_dispositivo, key, value)

    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo


##Eliminar dispositivo.

def eliminar_dispositivo(db: Session, dispositivo_id: int):
    db_device = db.query(Device).filter(Device.id == dispositivo_id).first()

    if db_device:
        db.delete(db_device)
        db.commit()
        return True

    return False