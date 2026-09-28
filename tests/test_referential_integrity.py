from framework.db_utils import fetch_all
from framework.validators import validate_referential_integrity


def test_customer_referential_integrity():

    source_ids = fetch_all(
        """
        SELECT customer_id
        FROM source_customers
        """
    )

    target_ids = fetch_all(
        """
        SELECT customer_id
        FROM target_customers
        """
    )

    source_ids = [row[0] for row in source_ids]
    target_ids = [row[0] for row in target_ids]

    validate_referential_integrity(source_ids, target_ids)