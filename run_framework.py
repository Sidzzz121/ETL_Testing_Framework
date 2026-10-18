
import subprocess
import sys
import html
from pathlib import Path

from framework.data_profiler import profile_source_data
from framework.logger import logger
from etl.load import run_etl


PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def main():
    logger.info("Starting ETL Testing Framework...")

    try:
        # Execute the ETL pipeline.
        run_etl()

        # Profile source data and detect anomalies.
        profile = profile_source_data()
        logger.info("Data profiling completed: %s", profile)

    except Exception:
        logger.exception("ETL or data profiling failed")
        sys.exit(1)

    # Run automated tests and generate reports.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--cov=etl",
            "--cov=framework",
            "--cov-append",
            "--cov-report=term-missing",
            f"--cov-report=html:{REPORT_DIR / 'coverage'}",
            f"--html={REPORT_DIR / 'etl_report.html'}",
            "--self-contained-html",
        ],
        cwd=PROJECT_ROOT,
    )

    report_path = REPORT_DIR / "etl_report.html"

    if report_path.exists():
        try:
            # Prepare profiling metrics.
            excluded_keys = {
                "amount_anomalies",
                "anomaly_count",
            }

            profiling_rows = "".join(
                "<tr>"
                f"<td>{html.escape(key.replace('_', ' ').title())}</td>"
                f"<td>{html.escape(str(value))}</td>"
                "</tr>"
                for key, value in profile.items()
                if key not in excluded_keys
            )

            # Prepare anomaly details.
            anomaly_values = profile.get("amount_anomalies", [])
            anomaly_count = profile.get(
                "anomaly_count",
                len(anomaly_values),
            )

            if anomaly_values:
                anomaly_details = "".join(
                    f"<li>{html.escape(str(value))}</li>"
                    for value in anomaly_values
                )
                anomaly_status = "Anomalies detected"
                status_color = "#b45309"
            else:
                anomaly_details = (
                    "<li>No amount anomalies detected.</li>"
                )
                anomaly_status = "No anomalies detected"
                status_color = "#15803d"

            # Prepare data for the data-quality bar chart.
            chart_metrics = [
                (
                    "Total Records",
                    profile.get("total_records", 0),
                ),
                (
                    "Valid Emails",
                    profile.get("valid_emails", 0),
                ),
                (
                    "Null Names",
                    profile.get("null_names", 0),
                ),
                (
                    "Null Emails",
                    profile.get("null_emails", 0),
                ),
                (
                    "Null Amounts",
                    profile.get("null_amounts", 0),
                ),
                (
                    "Amount Anomalies",
                    anomaly_count,
                ),
            ]

            # Safely convert metrics into numeric values.
            normalized_metrics = []

            for label, value in chart_metrics:
                try:
                    numeric_value = max(0, float(value))
                except (TypeError, ValueError):
                    numeric_value = 0

                normalized_metrics.append(
                    (label, value, numeric_value)
                )

            max_chart_value = max(
                (item[2] for item in normalized_metrics),
                default=1,
            )
            max_chart_value = max(max_chart_value, 1)

            # Create proportional bars using actual profile values.
            chart_rows = ""

            for label, display_value, numeric_value in normalized_metrics:
                bar_width = min(
                    100,
                    (numeric_value / max_chart_value) * 100,
                )

                bar_color = (
                    "#15803d"
                    if label == "Valid Emails"
                    else "#2563eb"
                )

                if label == "Amount Anomalies" and numeric_value > 0:
                    bar_color = "#b45309"

                chart_rows += f"""
                    <div style="margin: 16px 0;">
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            gap: 12px;
                            margin-bottom: 6px;
                            font-size: 14px;
                        ">
                            <span>{html.escape(label)}</span>
                            <strong>
                                {html.escape(str(display_value))}
                            </strong>
                        </div>

                        <div style="
                            width: 100%;
                            height: 18px;
                            background: #e2e8f0;
                            border-radius: 5px;
                            overflow: hidden;
                        ">
                            <div style="
                                width: {bar_width:.2f}%;
                                height: 18px;
                                background: {bar_color};
                                border-radius: 5px;
                            "></div>
                        </div>
                    </div>
                """

            # Build the dashboard.
            dashboard = f"""
            <section style="
                margin: 30px 8px;
                padding: 24px;
                font-family: Arial, sans-serif;
                color: #1f2937;
                background: #f8fafc;
                border: 1px solid #dbe3ec;
                border-radius: 12px;
            ">
                <h1 style="margin-top: 0;">
                    ETL Data Quality Dashboard
                </h1>

                <p>
                    Source data profiling and statistical anomaly
                    detection results.
                </p>

                <div style="
                    display: flex;
                    flex-wrap: wrap;
                    gap: 16px;
                    margin: 20px 0;
                ">
                    <div style="
                        background: white;
                        border: 1px solid #dbe3ec;
                        border-radius: 8px;
                        padding: 16px;
                        min-width: 150px;
                    ">
                        <div>Total Records</div>
                        <strong style="font-size: 26px;">
                            {html.escape(str(profile.get('total_records', 0)))}
                        </strong>
                    </div>

                    <div style="
                        background: white;
                        border: 1px solid #dbe3ec;
                        border-radius: 8px;
                        padding: 16px;
                        min-width: 150px;
                    ">
                        <div>Overall Data Quality</div>
                        <strong style="font-size: 26px;">
                            {html.escape(str(profile.get('overall_data_quality_score', 0)))}%
                        </strong>
                    </div>

                    <div style="
                        background: white;
                        border: 1px solid #dbe3ec;
                        border-radius: 8px;
                        padding: 16px;
                        min-width: 150px;
                    ">
                        <div>Amount Anomalies</div>
                        <strong style="
                            font-size: 26px;
                            color: {status_color};
                        ">
                            {html.escape(str(anomaly_count))}
                        </strong>
                    </div>
                </div>

                <div style="
                    margin: 24px 0;
                    padding: 20px;
                    background: white;
                    border: 1px solid #dbe3ec;
                    border-radius: 10px;
                ">
                    <h2 style="margin-top: 0;">
                        Data Quality Metrics Chart
                    </h2>

                    <p style="color: #64748b; font-size: 14px;">
                        Comparison of record counts, valid emails,
                        missing values, and detected anomalies.
                    </p>

                    {chart_rows}
                </div>

                <h2>Data Quality Metrics</h2>

                <table style="
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                ">
                    <thead>
                        <tr style="background: #e2e8f0;">
                            <th style="
                                border: 1px solid #cbd5e1;
                                padding: 10px;
                                text-align: left;
                            ">
                                Metric
                            </th>
                            <th style="
                                border: 1px solid #cbd5e1;
                                padding: 10px;
                                text-align: left;
                            ">
                                Value
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {profiling_rows}
                    </tbody>
                </table>

                <h2>Amount Anomaly Detection</h2>

                <p>
                    <strong>Method:</strong>
                    Interquartile Range (IQR)
                </p>

                <p style="color: {status_color};">
                    <strong>Status:</strong>
                    {html.escape(anomaly_status)}
                </p>

                <h3>Detected Amounts</h3>
                <ul>{anomaly_details}</ul>
            </section>
            """

            # Insert the dashboard before the closing body tag.
            html_content = report_path.read_text(
                encoding="utf-8"
            )

            if "</body>" in html_content:
                html_content = html_content.replace(
                    "</body>",
                    dashboard + "\n</body>",
                    1,
                )

                report_path.write_text(
                    html_content,
                    encoding="utf-8",
                )

                logger.info(
                    "Data quality dashboard and metrics chart "
                    "added to HTML report"
                )
            else:
                logger.warning(
                    "Could not find closing body tag in HTML report"
                )

        except Exception:
            logger.exception(
                "Could not add profiling results to HTML report"
            )

    # Preserve the original test execution exit status.
    if result.returncode == 0:
        logger.info(
            "ETL Testing Framework: All tests passed successfully"
        )
    else:
        logger.error(
            "ETL Testing Framework: Test execution failed "
            "with exit code %s",
            result.returncode,
        )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
