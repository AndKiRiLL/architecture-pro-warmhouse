from database import Database
from config import settings

# Создаём экземпляр базы данных с URL из переменной окружения
db = Database(settings.DATABASE_URL)