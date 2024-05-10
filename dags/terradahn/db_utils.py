import logging
import psycopg2

from .config import settings


def create_users_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY
            )
    """
    run_db_command(table_command)


def create_movies_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title VARCHAR (255) UNIQUE NOT NULL,
            genres VARCHAR (255) NOT NULL,
            average_rating NUMERIC(5,2) NOT NULL
        )
    """

    run_db_command(table_command)


def create_cbr_predictions_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS cbr_predictions (
            movie_id INTEGER NOT NULL,
            sim_movie_id INTEGER NOT NULL,
            score NUMERIC(5,2) NOT NULL
        )
    """
    index_command = """
        CREATE INDEX IF NOT EXISTS idx_cbr_predictions_movie_id ON cbr_predictions(movie_id)
    """

    run_db_command(table_command)
    run_db_command(index_command)


def create_svdpp_predictions_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS svdpp_predictions (
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            score NUMERIC(5,2) NOT NULL
        )
    """

    index_command = """
            CREATE INDEX IF NOT EXISTS idx_svdpp_predictions_user_id ON svdpp_predictions(user_id)
        """

    run_db_command(table_command)
    run_db_command(index_command)


def run_db_command(query):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**settings.postgres_config)
        cursor = conn.cursor()

        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
    except (psycopg2.DatabaseError, Exception) as error:
        logging.error("Error running query")
        logging.error(error)
        if conn is not None:
            conn.rollback()
            cursor.close()
            conn.close()
            logging.info("PostgreSQL connection is closed")
        raise error


def insert_dataframe(table, dataframe):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**settings.postgres_config)

        # Create a list of tuples from the dataframe values
        tuples = [tuple(x) for x in dataframe.to_numpy()]

        # Comma-separated dataframe columns
        cols = ','.join(list(dataframe.columns))

        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        cursor = conn.cursor()

        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
        cursor.close()
        conn.close()
    except (psycopg2.DatabaseError, Exception) as error:
        logging.error("Error running query")
        logging.error(error)
        if conn is not None:
            conn.rollback()
            cursor.close()
            conn.close()
            logging.info("PostgreSQL connection is closed")
        raise error
