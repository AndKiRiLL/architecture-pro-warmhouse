import asyncpg
from asyncpg import Pool
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from datetime import datetime
from models.telemetry import TelemetryCreateRequestModel, Telemetry, TelemetryResponse
from utils.config import settings

import random
from datetime import datetime, timezone
from utils.logger_config import logger

import asyncio

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

    async def health_check(self) -> bool:
        """Check database connection"""
        try:
            async with self.acquire() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def create_telemetry(self, device_id: int) -> Telemetry:
        """
        Создаёт телеметрию для устройства с переданным device_id.
        Генерирует случайную температуру от 15 до 25 градусов и текущее время.
        """
        # Генерируем случайную температуру (можно с десятыми долями)
        random_temp = round(random.uniform(15.0, 25.0), 1)
        
        # Текущее время в UTC
        now = datetime.now(timezone.utc)
        
        query = """
            INSERT INTO telemtry (device_id, device_type, value, unit, timestamp)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, device_id, device_type, value, unit, timestamp
        """
        
        async with self.acquire() as conn:
            row = await conn.fetchrow(
                query,
                device_id,           # $1
                'temperature',       # $2
                random_temp,         # $3
                '°C',                # $4
                now                  # $5
            )
            
            if not row:
                raise Exception("Failed to create telemetry")
            
            return Telemetry(
                id=row['id'],
                device_id=row['device_id'],
                device_type=row['device_type'],
                value=row['value'],
                unit=row['unit'],
                timestamp=row['timestamp']
            )

    async def get_telemetry_by_device_id(
        self, 
        device_id: int,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "timestamp DESC"
    ) -> List[TelemetryResponse]:
        """
        Получить всю телеметрию для устройства по device_id.
        
        Args:
            device_id: ID устройства
            limit: Количество записей (по умолчанию 100)
            offset: Смещение для пагинации
            order_by: Сортировка (по умолчанию по времени по убыванию)
        """
        query = f"""
            SELECT id, device_id, device_type, value, unit, timestamp
            FROM telemtry
            WHERE device_id = $1
            ORDER BY {order_by}
            LIMIT $2 OFFSET $3
        """
        
        async with self.acquire() as conn:
            rows = await conn.fetch(query, device_id, limit, offset)
            
            return [
                TelemetryResponse(
                    id=row['id'],
                    device_id=row['device_id'],
                    device_type=row['device_type'],
                    value=row['value'],
                    unit=row['unit'],
                    timestamp=row['timestamp']
                )
                for row in rows
            ]