
from framework.db_utils import fetch_all
from framework.validators import validate_no_nulls


def test_amount_is_valid():
    query = """
        SELECT customer_id, amount
        FROM target_customers
        WHERE amount IS NULL
           OR amount < 0
    """

    invalid_records = fetch_all(query)

    assert validate_no_nulls(invalid_records)
