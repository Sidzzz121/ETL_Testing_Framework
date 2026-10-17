
from framework.db_utils import fetch_all
from framework.validators import validate_no_duplicates


def test_duplicate_customer_ids():
    query = """
        SELECT customer_id
        FROM source_customers
        ORDER BY customer_id
    """

    records = fetch_all(query)

    assert validate_no_duplicates(records)
