
import pytest
from unittest.mock import MagicMock, patch

from etl.load import run_etl


def test_etl_database_connection_failure():
    with patch(
        "etl.load.psycopg2.connect",
        side_effect=Exception("Simulated database connection failure"),
    ):
        with pytest.raises(
            Exception,
            match="Simulated database connection failure",
        ):
            run_etl()

@patch("etl.load.psycopg2.connect")
def test_etl_with_empty_source_data(mock_connect):
    conn = MagicMock()
    cursor = MagicMock()

    mock_connect.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = []

    run_etl()

    cursor.executemany.assert_called_once()
    assert cursor.executemany.call_args[0][1] == []


@pytest.mark.parametrize(
    "amount, expected_segment",
    [
        (25000, "PREMIUM"),
        (15000, "STANDARD"),
        (5000, "BASIC"),
    ],
)
@patch("etl.load.psycopg2.connect")
def test_etl_customer_segmentation(
    mock_connect, amount, expected_segment
):
    conn = MagicMock()
    cursor = MagicMock()

    mock_connect.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = [
        (1, "Test Customer", "test@example.com", "Mumbai", amount)
    ]

    run_etl()

    inserted_records = cursor.executemany.call_args[0][1]
    assert inserted_records[0][5] == expected_segment
