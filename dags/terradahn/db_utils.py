import logging
import numpy as np
import psycopg2
from psycopg2.extensions import register_adapter, AsIs

from .config import settings

register_adapter(np.int64, AsIs)
register_adapter(np.float64, AsIs)


def get_columns_from_dataframe(dataframe):
    return ','.join(list(dataframe.columns))


def get_connection():
    return psycopg2.connect(dbname=settings.external_database_config.dbname, user=settings.external_database_config.user,
                            password=settings.external_database_config.password, host=settings.external_database_config.host)
    # return psycopg2.connect(dbname=settings.postgres_config.dbname, user=settings.postgres_config.user,
    #                         password=settings.postgres_config.password, host="postgres")



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
            title VARCHAR (255) NOT NULL,
            genres VARCHAR (255) NOT NULL,
            tmdb_id INTEGER NOT NULL,
            average_rating NUMERIC(5,2) NOT NULL
        )
    """

    run_db_command(table_command)


def create_cbr_predictions_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS cbr_predictions (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER NOT NULL,
            sim_movie_id INTEGER NOT NULL,
            score NUMERIC(5,2) NOT NULL,
            UNIQUE (movie_id, sim_movie_id)
        )
    """
    index_command = """
        CREATE INDEX IF NOT EXISTS idx_cbr_predictions_movie_id ON cbr_predictions(movie_id)
    """

    run_db_command(table_command)
    run_db_command(index_command)


def create_svd_predictions_table():
    table_command = """
        CREATE TABLE IF NOT EXISTS svd_predictions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            score NUMERIC(5,2) NOT NULL,
            UNIQUE (user_id, movie_id)
        )
    """

    index_command = """
            CREATE INDEX IF NOT EXISTS idx_svd_predictions_user_id ON svd_predictions(user_id)
        """

    run_db_command(table_command)
    run_db_command(index_command)


def run_db_command(query):
    conn = None
    cursor = None
    try:
        conn = get_connection()
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


def insert_dataframe(table, dataframe, query=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()

        # Create a list of tuples from the dataframe values
        tuples = [tuple(x) for x in dataframe.to_numpy()]

        if query is None:
            cols = get_columns_from_dataframe(dataframe)
            query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)

        # Comma-separated dataframe columns
        # cols = ','.join(list(dataframe.columns))

        # SQL query to execute
        # query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
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
