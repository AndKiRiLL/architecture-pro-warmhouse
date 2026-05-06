from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

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