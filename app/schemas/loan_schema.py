from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, Self

class LoanCreate(BaseModel):
    user_id: int
    device_id: int

class UserEnPrestamo(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}

class DeviceEnPrestamo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = {"from_attributes": True}

class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    user: UserEnPrestamo
    device: DeviceEnPrestamo

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def mapear_campos(cls, data: Self):
        if hasattr(data, "__dict__"):
            return {
                "loan_id": data.id,
                "status": data.status,
                "user": data.user,
                "device": data.device,
            }
        return data