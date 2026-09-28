import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("ETL_DB_HOST", "localhost"),
    "port": int(os.getenv("ETL_DB_PORT", "5432")),
    "user": os.getenv("ETL_DB_USER", "postgres"),
    "password": os.getenv("ETL_DB_PASSWORD"),
    "database": os.getenv("ETL_DB_NAME", "etl_testing_db"),
}