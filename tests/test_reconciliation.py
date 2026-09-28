from framework.db_utils import fetch_one
from framework.validators import validate_reconciliation


def test_amount_reconciliation():

    source_total = fetch_one(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM source_customers
        """
    )[0]

    target_total = fetch_one(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM target_customers
        """
    )[0]

    validate_reconciliation(source_total, target_total)