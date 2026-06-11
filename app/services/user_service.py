from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserPatch, UserUpdate, UserResponse


##Crear usuario.

def crear_usuario(db: Session, usuario_data: UserCreate):

    db_usuario = User(
        name=usuario_data.name,
        email=usuario_data.email,
        role=usuario_data.role,
        is_active=usuario_data.is_active
    )

    db.add(db_usuario)

    db.commit

    db.refresh(db_usuario)

    return db_usuario


##Listar usuarios.

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


##Buscar usuario por ID.

def obtener_usuario_id(db: Session, usuario_id: int):
    return db.query(User).filter(User.id == usuario_id).first()


##Buscar usuario por email.

def obtener_usuario_email(db: Session, usuario_email: str):
    return db.query(User).filter(User.email == usuario_email).first()


##Actualizar usuario completo.

def actualizar_usuario(db: Session, usuario_id: int, usuario_data: UserUpdate):
    
    db_usuario = db.query(User).filter(User.id == usuario_id).first()

    if db_usuario:
        db_usuario.name = usuario_data.name
        db_usuario.email = usuario_data.email
        db_usuario.role = usuario_data.role
        db_usuario.is_active = usuario_data.is_active

        # Confirmar cambios
        db.commit()
        db.refresh(db_usuario)

    return db_usuario


##Actualizar usuario parcial.

def actualizar_usuario_parcial(db: Session, usuario_id: int, usuario_data: UserPatch):

    update_data = usuario_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


##Eliminar usuario.

def eliminar_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(User).filter(User.id == usuario_id).first()

    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True

    return False


##Filtrar usuarios por rol.

def filtro_rol(db: Session, usuario_rol: str):

    return db.query(User).filter(
        User.role.contains(usuario_rol)
    ).all()


##Filtrar usuarios por estado.

def filtro_estado(db: Session, usuario_estado: bool):

    return db.query(User).filter(
        User.is_active.contains(usuario_estado)
    ).all()


##Ordenar usuarios por nombre o fecha de creación.

def usuarios_fecha_creacion(db: Session):

    return db.query(User).order_by(
        User.created_at.asc()
    ).all()
