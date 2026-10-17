
import subprocess
import sys
from pathlib import Path

from etl.load import run_etl

PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def main():
    print("Starting ETL Testing Framework...")

    try:
        run_etl()
    except Exception as error:
        print(f"ETL execution failed: {error}")
        sys.exit(1)

    result = subprocess.run([
        sys.executable,
        "-m",
        "pytest",
        "-v",
        f"--html={REPORT_DIR / 'etl_report.html'}",
        "--self-contained-html",
    ], cwd=PROJECT_ROOT)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
