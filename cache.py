import redis
import json
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host = os.getenv("REDIS_HOST", "localhost"),
            port = int(os.getenv("REDIS_PORT", 6379)),
            db = int(os.getenv("REDIS_DB", 0)),
            decode_responses=True
        )
        self.ttl = int(os.getenv("CACHE_TTL", 3600))

    def get(self, key):
        cached_data = self.redis_client.get(key)
        if cached_data:
            print(f"Кэш HIT для ключа: {key}")
            return json.loads(cached_data)
        print(f"Кэш MISS для ключа: {key}")
        return None

    def set(self, key, data):
        self.redis_client.setex(
            key,
            timedelta(seconds=self.ttl),
            json.dumps(data)
        )
        print(f"Сохранено в кэш: {key} (TTL: {self.ttl} сек)")

    def delete(self, key):
        self.redis_client.delete(key)
        print(f"Удален ключ из кэша {key}")

    def clear_all(self, key):
        self.redis_client.flushdb()
        print("Весь кэш очищен")

cache = RedisCache()
