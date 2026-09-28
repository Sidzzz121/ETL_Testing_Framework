from framework.db_utils import fetch_all
from framework.validators import validate_no_nulls


def test_source_null_values():
    query = """
        SELECT customer_id, customer_name, email, city, amount
        FROM source_customers
    """

    records = fetch_all(query)

    validate_no_nulls(records)