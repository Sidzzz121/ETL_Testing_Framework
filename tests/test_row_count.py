from framework.db_utils import fetch_one
from framework.validators import validate_row_count


def test_source_target_row_count():
    source_count = fetch_one(
        "SELECT COUNT(*) FROM source_customers"
    )[0]

    target_count = fetch_one(
        "SELECT COUNT(*) FROM target_customers"
    )[0]

    validate_row_count(source_count, target_count)