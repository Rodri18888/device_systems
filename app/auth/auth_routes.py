from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserRegister, Token
from app.schemas.user_schema import UserResponse
from app.models.user_model import User
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.dependencies.database_dependencies import get_db
from app.dependencies.auth_dependencies import get_current_active_user
from slowapi import Limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register",
    summary="Registrar un nuevo usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse)
@Limiter.limit("3/minute")    
async def register(usuario: UserRegister, db: Session = Depends(get_db)):
    existente = db.query(User).filter(User.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    db_user = User(
        name=usuario.name,
        email=usuario.email,
        hashed_password=get_password_hash(usuario.password),
        role=usuario.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login",
    summary="Iniciar sesion y obtener token JWT",
    response_model=Token)
@Limiter.limit("5/minute")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(User.email == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    token = create_access_token(data={"sub": usuario.email, "role": usuario.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me",
    summary="Obtener usuario autenticado",
    response_model=UserResponse)
async def me(current_user: User = Depends(get_current_active_user)):
    return current_user