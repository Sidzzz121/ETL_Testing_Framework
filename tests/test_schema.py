from framework.db_utils import fetch_all
from framework.validators import validate_schema


def test_source_table_schema():
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'source_customers'
        ORDER BY ordinal_position
    """

    columns = fetch_all(query)

    actual_columns = [row[0] for row in columns]

    expected_columns = [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "amount"
    ]

    validate_schema(actual_columns, expected_columns)