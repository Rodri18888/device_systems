from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import (
    crear_prestamo,
    obtener_prestamos,
    obtener_prestamo_id,
    obtener_prestamos_detalle,
    obtener_prestamos_usuario,
    obtener_prestamos_dispositivo,
    devolver_prestamo,
)
from app.models.user_model import User
from app.models.device_model import Device
from app.dependencies.database_dependencies import get_db
from app.dependencies.auth_dependencies import require_admin_or_support, get_current_active_user
from slowapi import Limiter

router = APIRouter()


# GET /loans/
@router.get("/loans/", tags=["Loans"],
    summary="Obtener todos los prestamos",
    description="Lista prestamos con filtros opcionales por estado, email de usuario o tipo de dispositivo",
    response_description="Prestamos obtenidos con exito",
    response_model=list[LoanResponse])
async def obtener_prestamos_endpoint(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return obtener_prestamos(
        db,
        skip=skip,
        limit=limit,
        status=status,
        user_email=user_email,
        device_type=device_type
    )


# GET /loans/details  — debe ir antes de /{loan_id}
@router.get("/loans/details", tags=["Loans"],
    summary="Obtener prestamos con detalle de usuario y dispositivo",
    description="Retorna prestamos con joins a usuarios y dispositivos. Acepta filtros opcionales.",
    response_description="Prestamos con detalle obtenidos con exito",
    response_model=list[LoanDetailResponse])
async def obtener_prestamos_detalle_endpoint(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support)
):
    return obtener_prestamos_detalle(db, status=status, user_email=user_email, device_type=device_type)


# GET /loans/{loan_id}
@router.get("/loans/{loan_id}", tags=["Loans"],
    summary="Obtener un prestamo por id",
    description="Obtiene un prestamo segun la id indicada",
    response_description="Prestamo obtenido con exito",
    response_model=LoanResponse)
async def obtener_prestamo_endpoint(loan_id: int, db: Session = Depends(get_db)):
    db_loan = obtener_prestamo_id(db=db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return db_loan


# POST /loans/
@router.post("/loans/", tags=["Loans"],
    summary="Crear un prestamo",
    description="Valida usuario, dispositivo y disponibilidad antes de crear el prestamo",
    response_description="Prestamo creado con exito",
    status_code=status.HTTP_201_CREATED,
    response_model=LoanResponse)
@Limiter.limit("10/minute")
async def crear_prestamo_endpoint(loan: LoanCreate, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    usuario = db.query(User).filter(User.id == loan.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    dispositivo = db.query(Device).filter(Device.id == loan.device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not dispositivo.is_available:
        raise HTTPException(status_code=400, detail="Dispositivo no disponible")

    return crear_prestamo(db=db, loan_data=loan)


# PATCH /loans/{loan_id}/return
@router.patch("/loans/{loan_id}/return", tags=["Loans"],
    summary="Registrar devolucion de un prestamo",
    description="Marca el prestamo como returned, asigna fecha de devolucion y libera el dispositivo",
    response_description="Devolucion registrada con exito",
    response_model=LoanResponse)
async def devolver_prestamo_endpoint(loan_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin_or_support)):
    db_loan = devolver_prestamo(db=db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return db_loan


# GET /users/{user_id}/loans
@router.get("/users/{user_id}/loans", tags=["Loans"],
    summary="Obtener prestamos de un usuario",
    description="Lista todos los prestamos asociados a un usuario",
    response_description="Prestamos del usuario obtenidos con exito",
    response_model=list[LoanResponse])
async def obtener_prestamos_usuario_endpoint(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obtener_prestamos_usuario(db=db, user_id=user_id)


# GET /devices/{device_id}/loans
@router.get("/devices/{device_id}/loans", tags=["Loans"],
    summary="Obtener prestamos de un dispositivo",
    description="Lista todos los prestamos asociados a un dispositivo",
    response_description="Prestamos del dispositivo obtenidos con exito",
    response_model=list[LoanResponse])
async def obtener_prestamos_dispositivo_endpoint(device_id: int, db: Session = Depends(get_db)):
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return obtener_prestamos_dispositivo(db=db, device_id=device_id)