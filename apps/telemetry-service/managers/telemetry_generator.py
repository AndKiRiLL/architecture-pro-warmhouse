# managers/telemetry_generator.py
import asyncio
import random
from datetime import datetime, timezone
from typing import Optional
from utils.logger_config import logger
from db.db_init import db
from models.device import Device  # Импортируйте вашу модель Device

class TelemetryGenerator:
    def __init__(self):
        self._running = False
        
    async def start(self):
        """Запускает генератор телеметрии"""
        self._running = True
        logger.info("🚀 Telemetry generator STARTED (direct DB mode)")
        
        while self._running:
            try:
                await self.generate_telemetry_for_all_devices()
            except Exception as e:
                logger.error(f"Error in telemetry generation cycle: {e}", exc_info=True)
            
            # Ждём 3 секунды перед следующим циклом
            await asyncio.sleep(3)
    
    async def stop(self):
        """Останавливает генератор телеметрии"""
        self._running = False
        logger.info("Telemetry generator stopped")
    
    async def get_all_devices(self) -> list:
        """Get all devices from the database"""
        try:
            query = """
                SELECT id, name, type, location, value, unit, status, last_updated, created_at
                FROM devices
                ORDER BY created_at DESC
            """
            
            async with db.acquire() as conn:
                rows = await conn.fetch(query)
                
                devices = []
                for row in rows:
                    devices.append(Device(
                        id=row['id'],
                        name=row['name'],
                        type=row['type'],
                        location=row['location'],
                        value=row['value'],
                        unit=row['unit'],
                        status=row['status'],
                        last_updated=row['last_updated'],
                        created_at=row['created_at']
                    ))
                
                logger.info(f"Retrieved {len(devices)} devices from database")
                return devices
                
        except Exception as e:
            logger.error(f"Failed to get devices from database: {e}", exc_info=True)
            return []
    
    async def create_telemetry(self, device_id: int) -> Optional[dict]:
        """Создаёт телеметрию для одного устройства напрямую в БД"""
        try:
            # Генерируем случайную температуру от 15 до 25
            temperature = round(random.uniform(15.0, 25.0), 1)
            # Убираем timezone - просто datetime.utcnow() без timezone
            now = datetime.utcnow()  # вместо datetime.now(timezone.utc)
            
            query = """
                INSERT INTO telemtry (device_id, device_type, value, unit, timestamp)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, device_id, device_type, value, unit, timestamp
            """
            
            async with db.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    device_id,
                    'temperature',
                    temperature,
                    '°C',
                    now
                )
                
                if row:
                    result = {
                        'id': row['id'],
                        'device_id': row['device_id'],
                        'device_type': row['device_type'],
                        'value': row['value'],
                        'unit': row['unit'],
                        'timestamp': row['timestamp']
                    }
                    logger.info(f"Device {device_id}: {temperature}°C (telemetry ID: {row['id']})")
                    return result
                else:
                    logger.error(f"Device {device_id}: INSERT returned no row")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to create telemetry for device {device_id}: {e}", exc_info=True)
            return None
    
    async def generate_telemetry_for_all_devices(self):
        """Генерирует телеметрию для всех устройств"""
        devices = await self.get_all_devices()
        
        if not devices:
            logger.warning("No devices found in database")
            return
        
        logger.info(f"Generating telemetry for {len(devices)} devices...")
        
        # Создаём телеметрию для каждого устройства параллельно
        tasks = []
        for device in devices:
            if device.id:  # Используем атрибут id объекта Device
                tasks.append(self.create_telemetry(device.id))
        
        if tasks:
            # Дожидаемся выполнения всех задач
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Считаем успешные
            success_count = 0
            fail_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    fail_count += 1
                    logger.error(f"Task {i} failed with exception: {result}")
                elif result is not None:
                    success_count += 1
                else:
                    fail_count += 1
            
            logger.info(f"Created telemetry for {success_count}/{len(tasks)} devices ({fail_count} failed)")