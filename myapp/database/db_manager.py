from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO
# 1. create_engine의 connection string을 환경변수로부터 읽어오도록 수정한다.
# 2. 현재 세팅된 기본 pool_size는 5이나, 실제 서버의 부하에 따라 적절한 값으로 수정한다.
class DatabaseManager:
    _instance = None
    Base = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Replace the connection string with your actual connection string
            engine = create_engine('postgresql://developer:devpassword@127.0.0.1:25000/developer')
            cls._instance._Session = sessionmaker(bind=engine)
        return cls._instance

    def get_session(self):
        return self._Session()