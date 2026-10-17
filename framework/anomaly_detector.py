
def detect_iqr_anomalies(values, multiplier=1.5):
    """Detect numeric outliers using the Interquartile Range (IQR)."""

    if multiplier <= 0:
        raise ValueError("Multiplier must be greater than zero.")

    numbers = sorted(
        float(value)
        for value in values
        if value is not None
    )

    if not numbers:
        return []

    def percentile(sorted_values, fraction):
        position = (len(sorted_values) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(sorted_values) - 1)
        weight = position - lower

        return (
            sorted_values[lower] * (1 - weight)
            + sorted_values[upper] * weight
        )

    q1 = percentile(numbers, 0.25)
    q3 = percentile(numbers, 0.75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    return [
        value
        for value in numbers
        if value < lower_bound or value > upper_bound
    ]

def explain_iqr_anomalies(values, multiplier=1.5):
    """Return anomaly details, including severity and IQR boundaries."""

    anomalies = detect_iqr_anomalies(values, multiplier)

    numbers = sorted(
        float(value)
        for value in values
        if value is not None
    )

    if not numbers or not anomalies:
        return []

    def percentile(sorted_values, fraction):
        position = (len(sorted_values) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(sorted_values) - 1)
        weight = position - lower

        return (
            sorted_values[lower] * (1 - weight)
            + sorted_values[upper] * weight
        )

    q1 = percentile(numbers, 0.25)
    q3 = percentile(numbers, 0.75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    details = []

    for value in anomalies:
        if value < lower_bound:
            distance = lower_bound - value
            direction = "below"
        else:
            distance = value - upper_bound
            direction = "above"

        details.append({
            "value": value,
            "severity": (
                "HIGH"
                if distance > iqr
                else "MEDIUM"
            ),
            "direction": direction,
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "reason": (
                f"Value {value} is {direction} the IQR boundary "
                f"({lower_bound:.2f} to {upper_bound:.2f})."
            ),
        })

    return details

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
