from typing import Optional, List, Dict, Any
from models.device import Device, DeviceCreateRequestModel
from db_init import db
import aiohttp

import aiohttp
from logger_config import logger
import os

TEMPERATURE_API_URL = os.getenv(
    "TEMPERATURE_SERVICE_URL",
    "http://temperature-api:8081"
)

async def get_temperature() -> float:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{TEMPERATURE_API_URL}/temperature") as response:
                if response.status == 200:
                    data = await response.json()
                    value = data.get("value", 0.0)
                    return float(value)
                else:
                    logger.error(f"Temperature API returned status {response.status}")
                    return 0.0
    except Exception as e:
        logger.error(f"Failed to get temperature from API: {e}")
        return 0.0


async def get_all_devices() -> List[Device]:
    return await db.get_all_devices()

async def get_device_by_id(device_id: int) -> Optional[Device]:
    device = await db.get_device_by_id(device_id)
    
    if device:
        device.value = await get_temperature()
    
    return device

async def create_device(device_data: DeviceCreateRequestModel) -> Device:
    return await db.create_device(device_data)

async def update_device(device_id: int, update_data: Dict[str, Any]) -> Optional[Device]:
    return await db.update_device(device_id, update_data)

async def delete_device(device_id: int) -> bool:
    return await db.delete_device(device_id)

async def update_device_status(device_id: int, status: str) -> Optional[Device]:
    return await db.update_device_status(device_id, status)