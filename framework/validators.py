def validate_row_count(source_count, target_count):
    """
    Validate that source and target have the same number of records.
    """
    assert source_count == target_count, (
        f"Row count mismatch: "
        f"Source={source_count}, Target={target_count}"
    )

    return True


def validate_data(source_data, target_data):
    """
    Validate that source and target data are identical.
    """
    assert source_data == target_data, (
        "Source and target data do not match"
    )

    return True


def validate_no_nulls(records):
    """
    Validate that the provided records contain no NULL values.
    """
    for record in records:
        assert all(value is not None for value in record), (
            f"NULL value found in record: {record}"
        )

    return True


def validate_no_duplicates(records):
    """
    Validate that there are no duplicate records.
    """
    assert len(records) == len(set(records)), (
        "Duplicate records found"
    )

    return True


def validate_schema(actual_columns, expected_columns):
    """
    Validate that actual table columns match the expected schema.
    """
    assert actual_columns == expected_columns, (
        f"Schema mismatch: "
        f"Actual={actual_columns}, Expected={expected_columns}"
    )

    return True


def validate_transformation(actual_data, expected_data):
    """
    Validate that transformed target data matches expected values.
    """
    assert actual_data == expected_data, (
        f"Transformation mismatch: "
        f"Actual={actual_data}, Expected={expected_data}"
    )

    return True


def validate_data_types(actual_types, expected_types):
    """
    Validate that actual column data types match the expected data types.
    """
    assert actual_types == expected_types, (
        f"Data type mismatch: "
        f"Actual={actual_types}, Expected={expected_types}"
    )

    return True


def validate_referential_integrity(source_ids, target_ids):
    """
    Validate that every target ID exists in the source data.
    """
    source_id_set = set(source_ids)

    invalid_ids = [
        target_id
        for target_id in target_ids
        if target_id not in source_id_set
    ]

    assert not invalid_ids, (
        f"Referential integrity violation. "
        f"Invalid target IDs: {invalid_ids}"
    )

    return True


def validate_reconciliation(source_total, target_total):
    """
    Validate that source and target totals reconcile.
    """
    assert source_total == target_total, (
        f"Reconciliation mismatch: "
        f"Source={source_total}, Target={target_total}"
    )

    return True