import redis

# TODO
# 1. redis가 아닌 별개의 캐시 서버를 사용하게 될 경우에 대응하기
# 편하게 수정할 필요가 있는가?
# 2. 키 만료 시간, host, port 등을 환경변수로부터 읽어오도록 수정한다.
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
            print(f"Session extended for {value}")
