from fastapi import APIRouter
from models.device import DeviceCreateRequestModel, Device, DeviceCreateResponseModel, DeviceUpdateRequestModel, DeviceStatusUpdateModel
from managers.device import create_device as _create_device
from managers.device import get_all_devices as _get_all_devices
from managers.device import get_device_by_id as _get_device_by_id
from managers.device import update_device as _update_device
from managers.device import delete_device as _delete_device
from managers.device import update_device_status as _update_device_status
from fastapi import HTTPException
from typing import List
from logger_config import logger

DeviceRouter = APIRouter()

@DeviceRouter.get("/devices", response_model=List[Device])
async def get_all_devices():
    try:
        devices = await _get_all_devices()
        logger.info(f"Retrieved {len(devices)} devices")
        return devices
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving devices: {str(e)}")

@DeviceRouter.get("/device/{device_id}", response_model=Device)
async def get_device(device_id: int):
    try:
        device = await _get_device_by_id(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        logger.info(f"Retrieved device: {device.id} - {device.name}")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving device {device_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving device: {str(e)}")

@DeviceRouter.post("/device/add", response_model=Device, status_code=201)
async def create_device(request: DeviceCreateRequestModel):
    try:
        device = await _create_device(request)
        logger.info(f"Device created: {device.id} - {device.name}")
        return device
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating device: {str(e)}")

@DeviceRouter.patch("/device/{device_id}", response_model=Device)
async def update_device(device_id: int, update_data: DeviceUpdateRequestModel):
    try:
        # Преобразуем модель в словарь, исключая None значения
        update_dict = update_data.dict(exclude_unset=True)
        
        device = await _update_device(device_id, update_dict)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        logger.info(f"Device updated: {device.id} - {device.name}")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating device: {str(e)}")

@DeviceRouter.delete("/device/{device_id}", status_code=204)
async def delete_device(device_id: int):
    try:
        deleted = await _delete_device(device_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Device not found")
        
        logger.info(f"Device deleted: {device_id}")
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting device: {str(e)}")

@DeviceRouter.patch("/device/{device_id}/status", response_model=Device)
async def update_device_status(device_id: int, status_data: DeviceStatusUpdateModel):
    try:
        device = await _update_device_status(device_id, status_data.status)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        logger.info(f"Device status updated: {device.id} - {device.status}")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating device status {device_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating device status: {str(e)}")