import os
from dotenv import load_dotenv

# Загружаем .env файл если есть (для локальной разработки)
load_dotenv()

class Settings:
    """Настройки приложения из переменных окружения"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/smarthome"
    )
    
    # Service config
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "50052"))
    
    # Другие настройки (если нужны)
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()