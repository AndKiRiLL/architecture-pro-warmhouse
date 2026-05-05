import asyncpg
from asyncpg import Pool
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from datetime import datetime
from models.device import DeviceCreateRequestModel, Device
from config import settings

import logging
import asyncio

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[Pool] = None

    async def connect(self):
        """Create connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info(f"Connected to database: {self.dsn}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection closed")

    @asynccontextmanager
    async def acquire(self):
        """Acquire connection from pool"""
        async with self.pool.acquire() as connection:
            yield connection

    async def get_all_devices(self) -> List[Device]:
        """Get all devices from the database"""
        query = """
            SELECT id, name, type, location, value, unit, status, last_updated, created_at
            FROM devices
            ORDER BY created_at DESC
        """
        
        async with self.acquire() as conn:
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
            
            return devices

    async def get_device_by_id(self, device_id: int) -> Optional[Device]:
        """Get a single device by ID"""
        query = """
            SELECT id, name, type, location, value, unit, status, last_updated, created_at
            FROM devices
            WHERE id = $1
        """
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(query, device_id)
            
            if not row:
                return None
            
            return Device(
                id=row['id'],
                name=row['name'],
                type=row['type'],
                location=row['location'],
                value=row['value'],
                unit=row['unit'],
                status=row['status'],
                last_updated=row['last_updated'],
                created_at=row['created_at']
            )

    async def create_device(self, device_data: DeviceCreateRequestModel) -> Device:
        """Create a new device in the database"""
        query = """
            INSERT INTO devices (name, type, location, unit, status, last_updated, created_at)
            VALUES ($1, $2, $3, $4, 'inactive', $5, $5)
            RETURNING id, name, type, location, value, unit, status, last_updated, created_at
        """
        
        now = datetime.utcnow()
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(
                query,
                device_data.name,
                device_data.type,
                device_data.location,
                device_data.unit,
                now
            )
            
            if not row:
                raise Exception("Failed to create device")
            
            return Device(
                id=row['id'],
                name=row['name'],
                type=row['type'],
                location=row['location'],
                value=row['value'],
                unit=row['unit'],
                status=row['status'],
                last_updated=row['last_updated'],
                created_at=row['created_at']
            )

    async def update_device(self, device_id: int, update_data: Dict[str, Any]) -> Optional[Device]:
        """
        Частичное обновление устройства
        update_data - словарь с полями для обновления
        """
        # Сначала проверяем существование устройства
        existing_device = await self.get_device_by_id(device_id)
        if not existing_device:
            return None
        
        # Строим динамический UPDATE запрос
        set_clauses = []
        values = []
        param_counter = 1
        
        # Маппинг разрешенных для обновления полей
        allowed_fields = {
            'name': 'name',
            'type': 'type', 
            'location': 'location',
            'unit': 'unit',
            'status': 'status',
            'value': 'value'
        }
        
        for field, db_column in allowed_fields.items():
            if field in update_data and update_data[field] is not None:
                set_clauses.append(f"{db_column} = ${param_counter}")
                values.append(update_data[field])
                param_counter += 1
        
        if not set_clauses:
            # Нечего обновлять
            return existing_device
        
        # Добавляем last_updated
        now = datetime.utcnow()
        set_clauses.append(f"last_updated = ${param_counter}")
        values.append(now)
        param_counter += 1
        
        # Добавляем device_id в конец
        values.append(device_id)
        
        query = f"""
            UPDATE devices 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_counter}
            RETURNING id, name, type, location, value, unit, status, last_updated, created_at
        """
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            
            if not row:
                return None
            
            return Device(
                id=row['id'],
                name=row['name'],
                type=row['type'],
                location=row['location'],
                value=row['value'],
                unit=row['unit'],
                status=row['status'],
                last_updated=row['last_updated'],
                created_at=row['created_at']
            )

    async def delete_device(self, device_id: int) -> bool:
        """
        Удаление устройства
        Возвращает True если устройство удалено, False если не найдено
        """
        query = """
            DELETE FROM devices 
            WHERE id = $1
            RETURNING id
        """
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(query, device_id)
            
            if not row:
                return False
            
            logger.info(f"Device deleted: {device_id}")
            return True

    async def update_device_status(self, device_id: int, status: str) -> Optional[Device]:
        """
        Обновление только статуса устройства (частый use-case)
        """
        query = """
            UPDATE devices 
            SET status = $1, last_updated = $2
            WHERE id = $3
            RETURNING id, name, type, location, value, unit, status, last_updated, created_at
        """
        
        now = datetime.utcnow()
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(query, status, now, device_id)
            
            if not row:
                return None
            
            return Device(
                id=row['id'],
                name=row['name'],
                type=row['type'],
                location=row['location'],
                value=row['value'],
                unit=row['unit'],
                status=row['status'],
                last_updated=row['last_updated'],
                created_at=row['created_at']
            )
    
    async def health_check(self) -> bool:
        """Check database connection"""
        try:
            async with self.acquire() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
