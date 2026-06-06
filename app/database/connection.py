from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Base de datos
DATABASE_URL = "sqlite:///./device_systems.db"

# Engine

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base

class Base(DeclarativeBase):
    pass

# Función para crear tablas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Sesion de base de datos
