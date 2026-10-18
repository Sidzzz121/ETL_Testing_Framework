
import pytest
from framework.anomaly_detector import detect_iqr_anomalies
from framework.anomaly_detector import explain_iqr_anomalies


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

def test_anomaly_includes_severity_and_explanation():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18, 100]

    result = explain_iqr_anomalies(values)

    assert len(result) == 1
    anomaly = result[0]
    assert anomaly["value"] == 100.0
    assert anomaly["severity"] == "HIGH"
    assert anomaly["direction"] == "above"
    assert anomaly["lower_bound"] < anomaly["upper_bound"]
    assert "IQR boundary" in anomaly["reason"]


def test_explanation_returns_empty_list_without_anomalies():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    assert explain_iqr_anomalies(values) == []

def test_detects_extreme_amount_anomaly():
    values = [100, 110, 120, 130, 140, 150, 160, 170, 180, 10000]

    anomalies = detect_iqr_anomalies(values)

    assert 10000.0 in anomalies


def test_detects_anomaly_below_lower_bound():
    values = [-10000, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    anomalies = detect_iqr_anomalies(values)

    assert -10000.0 in anomalies


def test_explains_anomaly_below_lower_bound():
    values = [-10000, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    result = explain_iqr_anomalies(values)

    assert len(result) == 1
    assert result[0]["value"] == -10000.0
    assert result[0]["direction"] == "below"
    assert result[0]["severity"] == "HIGH"
    assert "IQR boundary" in result[0]["reason"]


def test_explains_medium_severity_anomaly():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18, 24]

    result = explain_iqr_anomalies(values)

    assert len(result) == 1
    assert result[0]["value"] == 24.0
    assert result[0]["severity"] == "MEDIUM"
    assert result[0]["direction"] == "above"


def test_detects_anomalies_with_custom_multiplier():
    values = [10, 11, 12, 13, 14, 15, 16, 17, 18, 100]

    anomalies = detect_iqr_anomalies(values, multiplier=1.0)

    assert 100.0 in anomalies


def test_explanation_with_none_values():
    values = [10, 11, None, 12, 13, 14, 15, 16, 17, 100]

    result = explain_iqr_anomalies(values)

    assert len(result) == 1
    assert result[0]["value"] == 100.0


def test_detects_no_anomalies_for_single_value():
    assert detect_iqr_anomalies([10]) == []


def test_explanation_returns_empty_for_single_value():
    assert explain_iqr_anomalies([10]) == []
