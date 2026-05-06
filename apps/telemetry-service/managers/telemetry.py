from typing import Optional, List, Dict, Any
from models.telemetry import Telemetry, TelemetryCreateRequestModel
from db.db_init import db
import aiohttp
# from logger_config import logger
# import os

async def create_telemetry(telemetry_data: TelemetryCreateRequestModel) -> Telemetry:
    return await db.create_telemetry(telemetry_data)

async def get_telemetry_by_device_id(device_id: int) -> List[Telemetry]:
    telemetry_list = await db.get_telemetry_by_device_id(device_id)
    
    return telemetry_list