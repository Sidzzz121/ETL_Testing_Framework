
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

    # Add data profiling and anomaly results to the HTML report.
    report_path = REPORT_DIR / "etl_report.html"

    if report_path.exists():
        try:
            # Build the source data quality table.
            excluded_keys = {"amount_anomalies", "anomaly_count"}

            profiling_rows = "".join(
                "<tr>"
                f"<td>{html.escape(key.replace('_', ' ').title())}</td>"
                f"<td>{html.escape(str(value))}</td>"
                "</tr>"
                for key, value in profile.items()
                if key not in excluded_keys
            )

            # Prepare anomaly detection results.
            anomaly_values = profile.get("amount_anomalies", [])
            anomaly_count = profile.get(
                "anomaly_count", len(anomaly_values)
            )

            if anomaly_values:
                anomaly_details = "".join(
                    f"<li>{html.escape(str(value))}</li>"
                    for value in anomaly_values
                )
                anomaly_status = "Anomalies detected"
            else:
                anomaly_details = (
                    "<li>No amount anomalies detected.</li>"
                )
                anomaly_status = "No anomalies detected"

            profiling_section = f"""
            <section style="margin: 25px 8px; font-family: Arial, sans-serif;">
                <h2>Source Data Quality Profile</h2>
                <table style="border-collapse: collapse; min-width: 400px;">
                    <thead>
                        <tr>
                            <th style="border: 1px solid #ccc; padding: 8px;">
                                Metric
                            </th>
                            <th style="border: 1px solid #ccc; padding: 8px;">
                                Value
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {profiling_rows}
                    </tbody>
                </table>
            </section>
            """

            anomaly_section = f"""
            <section style="margin: 25px 8px; font-family: Arial, sans-serif;">
                <h2>Amount Anomaly Detection</h2>
                <p>
                    <strong>Detection method:</strong>
                    Interquartile Range (IQR)
                </p>
                <p>
                    <strong>Status:</strong>
                    {html.escape(anomaly_status)}
                </p>
                <p>
                    <strong>Anomaly count:</strong>
                    {anomaly_count}
                </p>
                <h3>Detected Amounts</h3>
                <ul>
                    {anomaly_details}
                </ul>
            </section>
            """

            html_content = report_path.read_text(encoding="utf-8")

            # Insert both sections before the closing body tag.
            html_content = html_content.replace(
                "</body>",
                profiling_section + anomaly_section + "\n</body>",
            )

            report_path.write_text(
                html_content,
                encoding="utf-8",
            )

            logger.info(
                "Data profiling and anomaly results added to HTML report"
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
