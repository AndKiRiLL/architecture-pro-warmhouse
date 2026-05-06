from db.database import Database
from utils.config import settings

# Создаём экземпляр базы данных с URL из переменной окружения
db = Database(settings.DATABASE_URL)