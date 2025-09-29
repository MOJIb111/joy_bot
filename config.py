import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    #токен бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    #база данных
    DB_CONFIG = {
        "dbname" : os.getenv("DB_NAME", "joyreactor_data"),
        "user": os.getenv("DB_USER", "saitama"),
        "password": os.getenv("DB_PASSWORD", "hungry"),
        "host": os.getenv("DB_HOST", "postgres"),
        "port": os.getenv("DB_PORT", "5432")
    }

    #redis кэш
    REDIS_CONFIG = {
        "host" : os.getenv("REDIS_HOST", "redis"),
        "port" : os.getenv("REDIS_PORT", 6379),
        "db" : os.getenv("REDIS_DB", 0),
        "decode_responses": True
    }

    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

config = Config()

