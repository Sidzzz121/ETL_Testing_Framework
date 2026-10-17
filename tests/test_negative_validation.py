
import pytest

from framework.validators import validate_no_nulls


def test_null_value_is_detected():
    invalid_records = [
        (1, "Rahul", "rahul@gmail.com"),
        (2, None, "priya@gmail.com"),
    ]

    with pytest.raises(AssertionError, match="NULL value found"):
        validate_no_nulls(invalid_records)
        
from framework.validators import validate_no_duplicates


def test_duplicate_records_are_detected():
    invalid_records = [
        (1,),
        (2,),
        (1,),
    ]

    with pytest.raises(AssertionError, match="Duplicate records found"):
        validate_no_duplicates(invalid_records)
        
from framework.validators import validate_email_format


def test_invalid_email_is_detected():
    invalid_emails = [
        "not-an-email",
        "missing-at-symbol.com",
        "user@",
    ]

    with pytest.raises(AssertionError):
        validate_email_format(invalid_emails)

def test_invalid_email_is_detected():
    invalid_emails = [
        "not-an-email",
        "missing-at-symbol.com",
        "user@",
    ]

    with pytest.raises(AssertionError, match="Invalid email format found"):
        validate_email_format(invalid_emails)        
        
        


