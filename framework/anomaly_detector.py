
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
