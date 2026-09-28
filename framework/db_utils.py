import psycopg2
from config.database import DB_CONFIG


def connect_db(database=None):
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=database or DB_CONFIG["database"]
    )


def execute_query(query, database=None):
    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, database=None):
    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, database=None):
    conn = connect_db(database)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()