from framework.db_utils import fetch_all


def test_amount_is_valid():
    query = """
        SELECT customer_id
        FROM target_customers
        WHERE amount IS NULL
           OR amount < 0
    """

    invalid_records = fetch_all(query)

    assert len(invalid_records) == 0