from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserMinimalResponse(BaseModel):
    id: int
    name: str 
    email: str

    model_config = ConfigDict(from_attributes=True)

class DeviceMinimalResponse(BaseModel):
    id: int
    name: str 
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoanCreate(LoanBase):
    user_id: int
    device_id: int
    status: str



class LoanUpdate(BaseModel):
    user_id: Optional[int] = None
    device_id: Optional[int] = None
    return_date: Optional[datetime] = None
    status: Optional[str] = None



class LoanResponse(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)



class LoanDetailResponse(LoanResponse):
    user: UserMinimalResponse
    device: DeviceMinimalResponse

    model_config = ConfigDict(from_attributes=True)