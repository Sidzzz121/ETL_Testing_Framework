
import pytest
from unittest.mock import patch

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
