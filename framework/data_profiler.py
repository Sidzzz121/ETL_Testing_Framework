from framework.db_utils import fetch_all
from framework.logger import logger


def profile_source_data():
    """Generate a data quality profile for source customer data."""

    query = """
        SELECT
            COUNT(*) AS total_records,
            COUNT(*) FILTER (
                WHERE customer_name IS NULL
            ) AS null_names,
            COUNT(*) FILTER (
                WHERE email IS NULL
            ) AS null_emails,
            COUNT(*) FILTER (
                WHERE amount IS NULL
            ) AS null_amounts,
            COUNT(DISTINCT customer_id) AS unique_customer_ids,
            MIN(amount) AS minimum_amount,
            MAX(amount) AS maximum_amount,
            AVG(amount) AS average_amount,
            COUNT(*) FILTER (
                WHERE email IS NOT NULL
                AND email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+[.][A-Z]{2,}$'
            ) AS valid_emails
        FROM source_customers;
    """

    result = fetch_all(query)

    if not result:
        raise ValueError("Data profiling query returned no results.")

    profile = result[0]

    total_records = profile[0]
    null_names = profile[1]
    null_emails = profile[2]
    null_amounts = profile[3]
    unique_customer_ids = profile[4]
    valid_emails = profile[8]

    if total_records:
        total_required_values = total_records * 3
        missing_values = null_names + null_emails + null_amounts

        completeness_score = (
            (total_required_values - missing_values)
            / total_required_values
        ) * 100

        uniqueness_score = (
            unique_customer_ids / total_records
        ) * 100

        validity_score = (
            valid_emails / total_records
        ) * 100

        overall_score = (
            completeness_score
            + uniqueness_score
            + validity_score
        ) / 3
    else:
        completeness_score = 100.0
        uniqueness_score = 100.0
        validity_score = 100.0
        overall_score = 100.0

    report = {
        "total_records": total_records,
        "null_names": null_names,
        "null_emails": null_emails,
        "null_amounts": null_amounts,
        "unique_customer_ids": unique_customer_ids,
        "minimum_amount": (
            float(profile[5]) if profile[5] is not None else None
        ),
        "maximum_amount": (
            float(profile[6]) if profile[6] is not None else None
        ),
        "average_amount": (
            float(profile[7]) if profile[7] is not None else None
        ),
        "valid_emails": valid_emails,
        "completeness_score": round(completeness_score, 2),
        "uniqueness_score": round(uniqueness_score, 2),
        "validity_score": round(validity_score, 2),
        "overall_data_quality_score": round(overall_score, 2),
    }

    logger.info("Source data profile: %s", report)

    return report
