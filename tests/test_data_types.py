from framework.db_utils import fetch_all
from framework.validators import validate_data_types


def test_target_data_types():
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'target_customers'
        ORDER BY ordinal_position
    """

    columns = fetch_all(query)

    actual_types = [(row[0], row[1]) for row in columns]

    expected_types = [
        ("customer_id", "integer"),
        ("customer_name", "character varying"),
        ("email", "character varying"),
        ("city", "character varying"),
        ("amount", "numeric"),
        ("customer_segment", "character varying")
    ]

    validate_data_types(actual_types, expected_types)