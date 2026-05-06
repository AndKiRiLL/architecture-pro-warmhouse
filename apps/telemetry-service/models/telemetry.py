from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TelemetryBase(BaseModel):
    device_id: int
    device_type: str = 'temperature'
    value: float
    unit: str = '°C'


class TelemetryCreate(TelemetryBase):
    """Модель для создания телеметрии"""
    pass


class TelemetryCreateRequestModel(TelemetryBase):
    """Модель запроса (можно использовать, если нужно передавать данные)"""
    device_id: Optional[int] = None  # Будет переопределён из endpoint


class TelemetryResponse(TelemetryBase):
    """Модель ответа с ID и временной меткой"""
    id: int 
    device_id: int
    device_type: str
    value: float
    unit: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class Telemetry(TelemetryResponse):
    """Полная модель телеметрии (как вы использовали в коде)"""
    device_id: int
    
    class Config:
        from_attributes = True