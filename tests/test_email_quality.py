
from framework.db_utils import fetch_all
from framework.validators import validate_no_nulls


def test_customer_email_format():
    query = """
        SELECT customer_id, email
        FROM source_customers
        WHERE email IS NULL
           OR email NOT LIKE '%_@_%._%'
    """

    invalid_records = fetch_all(query)

    assert validate_no_nulls(invalid_records)
