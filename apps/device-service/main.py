from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from config import settings
from logger_config import logger

from db_init import db
from app.fastapi import construct

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting up device-service...")
    logger.info(f"Database URL: {settings.DATABASE_URL.replace('://', '://***@')}")  # Логируем без пароля
    await db.connect()
    logger.info("Device-service started successfully")
    yield
    # Shutdown
    logger.info("Shutting down device-service...")
    await db.close()
    logger.info("Device-service shutdown complete")


app: FastAPI = construct(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )