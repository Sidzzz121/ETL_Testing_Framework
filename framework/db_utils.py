import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def connect_db(database=None):
    """
    Create and return a PostgreSQL database connection.
    """

    return psycopg2.connect(
        host=os.getenv("ETL_DB_HOST"),
        port=os.getenv("ETL_DB_PORT"),
        user=os.getenv("ETL_DB_USER"),
        password=os.getenv("ETL_DB_PASSWORD"),
        dbname=database or "etl_testing_db"
    )


def execute_query(query, database=None):
    """
    Execute a SQL query without returning data.
    """

    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, database=None):
    """
    Execute a SELECT query and return all rows.
    """

    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, database=None):
    """
    Execute a SELECT query and return one row.
    """

    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()