from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Replace the connection string with your actual connection string
            engine = create_engine('postgresql://developer:devpassword@127.0.0.1:25000/developer')
            cls._instance._Session = sessionmaker(bind=engine)
        return cls._instance

    def get_session(self):
        return self._Session()