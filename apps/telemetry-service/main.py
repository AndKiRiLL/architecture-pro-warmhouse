# main.py
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from utils.config import settings
from utils.logger_config import logger
from managers.telemetry_generator import TelemetryGenerator
from db.db_init import db
from app.fastapi import construct

# Создаём генератор (без параметров, так как он использует прямой доступ к БД)
telemetry_generator = TelemetryGenerator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting up telemetry-service...")
    logger.info(f"Database URL: {settings.DATABASE_URL.replace('://', '://***@')}")
    
    # Подключаемся к БД
    await db.connect()
    logger.info("Database connected")
    
    # Запускаем генератор телеметрии как фоновую задачу
    generator_task = asyncio.create_task(telemetry_generator.start())
    logger.info("Telemetry generator started as background task")
    
    logger.info("Telemetry-service started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down telemetry-service...")
    
    # Останавливаем генератор
    await telemetry_generator.stop()
    generator_task.cancel()
    try:
        await generator_task
    except asyncio.CancelledError:
        logger.info("Generator task cancelled")
    
    # Закрываем соединение с БД
    await db.close()
    logger.info("Database connection closed")
    logger.info("Telemetry-service shutdown complete")

app: FastAPI = construct(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )