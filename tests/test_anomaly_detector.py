
import pytest
from framework.anomaly_detector import detect_iqr_anomalies
from framework.anomaly_detector import detect_iqr_anomalies


def test_detects_high_outlier():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18, 100]

    assert detect_iqr_anomalies(values) == [100.0]


def test_returns_empty_for_normal_values():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    assert detect_iqr_anomalies(values) == []


def test_handles_empty_input():
    assert detect_iqr_anomalies([]) == []


def test_ignores_none_values():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18, None]

    assert detect_iqr_anomalies(values) == []


def test_rejects_invalid_multiplier():
    with pytest.raises(ValueError):
        detect_iqr_anomalies([10, 20, 30], multiplier=0)
