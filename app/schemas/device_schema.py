from typing import Literal, Optional
from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    name = str = Field(min_length=3)
    serial_number = int
    device_type = str = Field(min_length=3)
    brand =  str = Field(min_length=3)
    is_available = bool


class DeviceUpdate(BaseModel):
    name = str = Field(min_length=3)
    serial_number = Optional[int] = None
    device_type = str = Field(min_length=3)
    brand =  str = Field(min_length=3)
    is_available = bool


class DevicePatch(BaseModel):
    name = Optional[str] = Field(default=None, min_length=3)
    serial_number = Optional[int] = None
    device_type = Optional[str] = Field(default=None, min_length=3)
    brand =  Optional[str] = Field(default=None, min_length=3)
    is_available = Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name = str 
    serial_number = int
    device_type = str 
    brand =  str 
    is_available = bool = True

    class Config:
        from_attributes = True



