import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    #токен бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    #база данных
    DB_CONFIG = {
        "dbname" : os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }

    #redis кэш
    REDIS_CONFIG = {
        "host" : os.getenv("REDIS_HOST"),
        "port" : os.getenv("REDIS_PORT"),
        "db" : os.getenv("REDIS_DB"),
        "decode_responses": True
    }

    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

config = Config()

