
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_db(database=None):
    return psycopg2.connect(
        host=os.getenv("ETL_DB_HOST"),
        port=os.getenv("ETL_DB_PORT"),
        user=os.getenv("ETL_DB_USER"),
        password=os.getenv("ETL_DB_PASSWORD"),
        dbname=database or "etl_testing_db",
    )


def execute_query(query, database=None):
    conn = connect_db(database)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
    finally:
        conn.close()


def fetch_all(query, database=None):
    conn = connect_db(database)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        conn.close()


def fetch_one(query, database=None):
    conn = connect_db(database)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()
    finally:
        conn.close()

