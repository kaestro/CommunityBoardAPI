import psycopg2

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = psycopg2.connect(
                host="127.0.0.1",
                port=25000,
                dbname="developer",
                user="developer",
                password="devpassword"
            )
        return cls._instance

    def execute_query(self, query):
        cur = self._conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result