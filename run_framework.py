
import subprocess
import sys
from pathlib import Path

from coverage import Coverage

from framework.logger import logger
from etl.load import run_etl


PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def main():
    logger.info("Starting ETL Testing Framework...")

    # Start code coverage before executing the ETL pipeline.
    coverage = Coverage(
        source=["etl", "framework"],
        omit=["*/__init__.py"],
    )
    coverage.start()

    try:
        run_etl()
    except Exception:
        logger.exception("ETL execution failed")
        coverage.stop()
        coverage.save()
        sys.exit(1)

    coverage.stop()
    coverage.save()

    # Run the automated test suite and generate reports.
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
