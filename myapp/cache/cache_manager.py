import redis

# 현재는 redis라는 커다란 객체를 session을 유지하는 key, value
# 저장소로 사용하고 있고, 이는 비효율적이다.
# 이를 해결하기 위해 추후에 다른 캐시들과 함께 사용할 확장성 있는
# 형태로의 리팩토링이 필요하다.
class CacheManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis = redis.Redis(host='127.0.0.1', port=25100, db=0)
        return cls._instance

    # key는 session_id, value는 email이다.
    def set(self, key, value, expire_time=3600):
        self._redis.set(key, value, expire_time)

    def get(self, key):
        return self._redis.get(key)
    
    def delete(self, key):
        self._redis.delete(key)

    def extend_session(self, key, expire_time=3600):
        value = self._redis.get(key)
        if value is not None:
            self._redis.set(key, value, expire_time)