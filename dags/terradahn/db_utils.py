import logging
import psycopg2

from .config import postgres_config

class Database:
    def __init__(self):
        conn = psycopg2.connect(**postgres_config)
        self.connection = conn
        logging.info("PostgreSQL connection is open")

    def close_connection():
        if self.connection is not None: 
                self.connection.close()
                logging.info("PostgreSQL connection is closed")

    def run_operation(self, queries: list[dict[str, tuple]]):
        try:

            cursor = self.connection.cursor()

            for query in queries:
                cursor.execute(query["command"],query["values"])
            
            self.connection.commit()
            cursor.close()
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Error running query")
            logging.error(error)
            self.close_connection()
            raise error

    def insert_one(self, query: dict[str, tuple]):
        self.run_operation([query])

    def insert_many(self, queries):
        self.run_operation(queries)

    def create_table(self, query):
        self.run_operation([query])


def create_users_table():
    user_table_creation_command = """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY
                    )
                """
    db = Database()
    db.create_table(user_table_creation_command)
    db.close_connection()
