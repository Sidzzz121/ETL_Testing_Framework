from framework.db_utils import fetch_all
from framework.validators import validate_transformation


def test_customer_segment_transformation():

    actual_data = fetch_all(
        """
        SELECT customer_id, customer_segment
        FROM target_customers
        ORDER BY customer_id
        """
    )

    expected_data = [
        (1, "STANDARD"),
        (2, "PREMIUM"),
        (3, "STANDARD"),
        (4, "PREMIUM"),
        (5, "STANDARD")
    ]

    validate_transformation(actual_data, expected_data)