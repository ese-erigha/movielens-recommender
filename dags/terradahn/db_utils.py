import psycopg2

db_config = {
    "user": "airflow",
    "password": "airflow",
    "database": "ariflow"
}

user_table_creation_command = """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY
                    )
                """

class Database:
    def __init__(self):
        conn = psycopg2.connect(**db_config)
        self.connection = conn
        print("PostgreSQL connection is open")

    def close_connection():
        if self.connection is not None: 
                self.connection.close()
                print("PostgreSQL connection is closed")

    def run_operation(self, queries: List[Dict[str, tuple]]):
        try:

            cursor = self.connection.cursor()

            for query in queries:
                cursor.execute(query["command"],query["values"])
            
            self.connection.commit()
            cursor.close()
        except (psycopg2.DatabaseError, Exception) as error:
            print("Error running query")
            print(error)
            self.close_connection()
            raise error

    def insert_one(self, query: Dict[str, tuple]):
        self.run_operation([query])

    def insert_many(self, queries):
        self.run_operation(queries)

    def create_table(self, query):
        self.run_operation([query])


def create_users_table():

    db = Database()
    db.create_table(user_table_creation_command)
    db.close_connection()
