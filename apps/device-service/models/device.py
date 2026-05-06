from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class DeviceCreateRequestModel(BaseModel):
    name: str
    type: str
    location: str
    unit: str

class DeviceCreateResponseModel(BaseModel):
    id: int
    message: str

class DeviceUpdateRequestModel(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = None
    location: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None

class DeviceStatusUpdateModel(BaseModel):
    status: str = Field(..., pattern="^(active|inactive|error)$")

class Device(BaseModel):
    id: int
    name: str
    type: str
    location: str
    value: Optional[float] = None
    unit: str
    status: DeviceStatus
    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True