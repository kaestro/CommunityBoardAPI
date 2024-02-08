import redis

class CacheManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis = redis.Redis(host='127.0.0.1', port=25100, db=0)
        return cls._instance

    def set(self, key, value):
        self._redis.set(key, value)

    def get(self, key):
        return self._redis.get(key)