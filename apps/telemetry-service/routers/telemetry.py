from fastapi import APIRouter
from models.telemetry import Telemetry, TelemetryResponse
from managers.telemetry import get_telemetry_by_device_id as _get_telemetry_by_device_id
from typing import List
from fastapi import HTTPException
from utils.logger_config import logger

TelemetryRouter = APIRouter()

@TelemetryRouter.get("/telemetry/{device_id}", response_model=List[Telemetry])
async def get_telemetry(device_id: int):
    try:
        telemetry = await _get_telemetry_by_device_id(device_id)
        if not telemetry:
            raise HTTPException(status_code=404, detail="Telemetry not found")
        return telemetry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving telemetry {device_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving telemetry: {str(e)}")