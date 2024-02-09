from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO
# 1. singleton pattern을 사용해서 구현된 객체를, 의존성 주입을 통해
#   다른 객체에 주입할 수 있도록 수정한다. 대신 연결 수 제한 등을 고려해야 한다.
# 2. create_engine의 connection string을 환경변수로부터 읽어오도록 수정한다.
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