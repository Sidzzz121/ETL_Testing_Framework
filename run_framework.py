
import subprocess
import sys
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

        # Profile source data.
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

    # Add profiling results to the HTML test report.
    report_path = REPORT_DIR / "etl_report.html"

    if report_path.exists():
        try:
            profiling_rows = "".join(
                f"<tr><td>{key.replace('_', ' ').title()}</td>"
                f"<td>{value}</td></tr>"
                for key, value in profile.items()
            )

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

            html = report_path.read_text(encoding="utf-8")
            html = html.replace(
                "</body>",
                profiling_section + "\n</body>",
            )
            report_path.write_text(html, encoding="utf-8")

            logger.info("Data profiling added to HTML test report")

        except Exception:
            logger.exception("Could not add profiling results to HTML report")

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
