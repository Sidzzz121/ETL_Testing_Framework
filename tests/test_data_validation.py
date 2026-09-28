from framework.db_utils import fetch_all
from framework.validators import validate_data


def test_source_target_data():
    source_data = fetch_all(
        """
        SELECT customer_id, customer_name, email, city, amount
        FROM source_customers
        ORDER BY customer_id
        """
    )

    target_data = fetch_all(
        """
        SELECT customer_id, customer_name, email, city, amount
        FROM target_customers
        ORDER BY customer_id
        """
    )

    validate_data(source_data, target_data)