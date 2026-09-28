import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def run_etl():
    conn = psycopg2.connect(
        host=os.getenv("ETL_DB_HOST"),
        port=os.getenv("ETL_DB_PORT"),
        user=os.getenv("ETL_DB_USER"),
        password=os.getenv("ETL_DB_PASSWORD"),
        dbname="etl_testing_db"
    )

    try:
        with conn:
            with conn.cursor() as cur:

                # Extract
                cur.execute("""
                    SELECT customer_id, customer_name,
                           email, city, amount
                    FROM source_customers
                    ORDER BY customer_id
                """)

                records = cur.fetchall()
                print(f"Extracted {len(records)} records")

                # Transform
                transformed_records = []

                for record in records:
                    customer_id, customer_name, email, city, amount = record

                    if amount >= 20000:
                        customer_segment = "PREMIUM"
                    elif amount >= 10000:
                        customer_segment = "STANDARD"
                    else:
                        customer_segment = "BASIC"

                    transformed_records.append(
                        (
                            customer_id,
                            customer_name,
                            email,
                            city,
                            amount,
                            customer_segment
                        )
                    )

                print(
                    f"Transformed {len(transformed_records)} records"
                )

                # Load
                cur.execute("DELETE FROM target_customers")

                cur.executemany("""
                    INSERT INTO target_customers
                    (customer_id, customer_name,
                     email, city, amount, customer_segment)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, transformed_records)

                print(
                    f"Loaded {len(transformed_records)} records"
                )

        print("ETL PROCESS COMPLETED SUCCESSFULLY")

    finally:
        conn.close()


if __name__ == "__main__":
    run_etl()