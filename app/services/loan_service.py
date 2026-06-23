from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate
from datetime import datetime


def crear_prestamo(db: Session, loan_data: LoanCreate):
    db_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )
    db.add(db_loan)

    dispositivo = db.query(Device).filter(Device.id == loan_data.device_id).first()
    dispositivo.is_available = False

    db.commit()
    db.refresh(db_loan)
    return db_loan


def obtener_prestamos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = db.query(Loan)

    if user_email:
        query = query.join(User, Loan.user_id == User.id)
        query = query.filter(User.email.ilike(f"%{user_email}%"))

    if device_type:
        query = query.join(Device, Loan.device_id == Device.id)
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))

    if status:
        query = query.filter(Loan.status == status)

    return query.offset(skip).limit(limit).all()


def obtener_prestamo_id(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()


def obtener_prestamos_detalle(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    filtros = []
    if status:
        filtros.append(Loan.status == status)
    if user_email:
        filtros.append(User.email.ilike(f"%{user_email}%"))
    if device_type:
        filtros.append(Device.device_type.ilike(f"%{device_type}%"))

    if filtros:
        query = query.where(and_(*filtros))

    return query.all()


def obtener_prestamos_usuario(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def obtener_prestamos_dispositivo(db: Session, device_id: int):
    return db.query(Loan).filter(Loan.device_id == device_id).all()


def devolver_prestamo(db: Session, loan_id: int):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not db_loan:
        return None

    dispositivo = db.query(Device).filter(Device.id == db_loan.device_id).first()

    db_loan.status = "returned"
    db_loan.return_date = datetime.utcnow()
    dispositivo.is_available = True

    db.commit()
    db.refresh(db_loan)
    return db_loan