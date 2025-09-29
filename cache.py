import redis
import json
from datetime import timedelta
from config import config

class RedisCache:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
            host = config.REDIS_CONFIG["host"],
            port = config.REDIS_CONFIG["port"],
            db = config.REDIS_CONFIG["db"],
            decode_responses=config.REDIS_CONFIG["decode_responses"],
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
            self.redis_client.ping()
            print("✅ Подключение к Redis установлено")

        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"❌ Ошибка подключения к Redis: {e}")
            self.redis_client = None

    def get(self, key):
        if not self.redis_client:
            return None
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except (redis.RedisError, json.JSONDecodeError) as e:
            print(f"❌ Ошибка получения из кэша: {e}")
            return None

    def set(self, key, value, expire_time=None):
        if not self.redis_client:
            return
        try:
            if expire_time is None:
                expire_time = config.CACHE_TTL
            self.redis_client.setex(
                key,
                expire_time,
                json.dumps(value, default=str)
            )
        except redis.RedisError as e:
            print(f"❌ Ошибка сохранения в кэш: {e}")

    def delete(self, key):
        if not self.redis_client:
            return
        try:
            self.redis_client.delete(key)
            print(f"✅ Ключ {key} удален из кэша")
        except redis.RedisError as e:
            print(f"❌ Ошибка удаления из кэша: {e}")

cache = RedisCache()
