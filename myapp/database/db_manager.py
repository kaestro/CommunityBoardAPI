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

    def execute_query(self, query, params):
        try:
            with self._conn.cursor() as cur:
                cur.execute(query, params)
                if query.lower().startswith("select"):
                    result = cur.fetchall()
                else:
                    result = None
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(f"An error occurred: {e}")
            result = None
        return result        