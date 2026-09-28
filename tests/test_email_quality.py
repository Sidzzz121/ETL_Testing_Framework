from framework.db_utils import fetch_all


def test_customer_email_format():
    query = """
        SELECT customer_id
        FROM target_customers
        WHERE email IS NULL
           OR email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'
    """

    invalid_emails = fetch_all(query)

    assert len(invalid_emails) == 0, (
        f"Invalid email records found: {invalid_emails}"
    )