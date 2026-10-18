# Automated ETL Testing Framework

## 1. Project Overview

The Automated ETL Testing Framework is a Python-based application designed to automate data quality validation and transformation testing in an Extract, Transform, Load (ETL) pipeline.

The framework extracts customer records from a PostgreSQL source table, applies transformation rules, loads the processed records into a target table, and executes automated validation tests using Pytest.

It also performs source data profiling, detects numerical anomalies using the Interquartile Range (IQR) method, and generates an HTML report containing test results and a data quality dashboard.

## 2. Problem Statement

Manual ETL testing requires considerable effort to verify data completeness, uniqueness, accuracy, consistency, and transformation correctness. Repeated manual validation can be time-consuming and may allow data quality defects to go undetected.

This project addresses these challenges by implementing a reusable automated framework for ETL validation, data profiling, anomaly detection, and test reporting.

## 3. Objectives

- Automate ETL data validation and transformation testing.
- Verify source and target record counts.
- Detect null values, duplicate records, and invalid email formats.
- Validate database schemas and data types.
- Verify customer segmentation and transformation rules.
- Check referential integrity and amount reconciliation.
- Profile source data and detect numerical anomalies using IQR.
- Generate HTML test reports and code coverage reports.
- Execute automated tests through GitHub Actions CI.

## 4. Technology Stack

- Python 3.12
- PostgreSQL
- pgAdmin 4
- Pytest
- pytest-html
- pytest-cov
- psycopg2
- python-dotenv
- Git and GitHub
- GitHub Actions

## 5. System Architecture

The framework follows an ETL testing workflow consisting of source data extraction, transformation, target loading, data profiling, automated validation, anomaly detection, and reporting.

[View the ETL Testing Framework Architecture](https://github.com/Sidzzz121/ETL_Testing_Framework/blob/main/docs/architecture.md)

## 6. Project Structure

```text
ETL_Testing_Framework/
├── .github/
│   └── workflows/
│       └── etl-tests.yml
├── config/
├── docs/
│   └── architecture.md
├── etl/
│   └── load.py
├── framework/
│   ├── __init__.py
│   ├── anomaly_detector.py
│   ├── data_profiler.py
│   ├── db_utils.py
│   ├── logger.py
│   └── validators.py
├── logs/
├── reports/
│   ├── coverage/
│   └── etl_report.html
├── tests/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run_framework.py
```

## 7. Prerequisites

- Python 3.12 or a compatible version
- PostgreSQL
- Git
- The Python dependencies listed in `requirements.txt`

## 8. Configuration

Create a `.env` file in the project root and configure your local PostgreSQL connection:

```text
ETL_DB_HOST=localhost
ETL_DB_PORT=5432
ETL_DB_USER=postgres
ETL_DB_PASSWORD=your_local_password
ETL_DB_NAME=etl_testing_db
```

Replace the example password with your own local database password. Keep `.env` out of version control and never publish database credentials.

## 9. Installation and Execution

Activate your existing virtual environment, if it is not already active.

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure PostgreSQL is running and the required source and target tables exist.

Run the framework:

```bash
python run_framework.py
```

The runner executes the ETL pipeline, profiles source data, runs the automated test suite, and generates the reports.

## 10. Automated Test Coverage

The test suite validates:

- Source and target row counts
- Data reconciliation
- Null values and duplicate records
- Email format and amount quality
- Source and target schemas
- Data types
- Transformation logic
- Referential integrity
- Negative validation scenarios
- ETL database connection failure handling
- IQR anomaly detection, severity, and explanations
- Data profiling results

## 11. Data Profiling and Anomaly Detection

The framework calculates source data quality metrics, including record counts, null counts, unique customer IDs, amount statistics, and valid email counts.

It uses the Interquartile Range (IQR) method to identify unusually low or high numerical values. The anomaly explanation function reports the detected value, severity, direction, and IQR boundaries.

## 12. Reports and Results

The framework generates:

- **HTML test report:** `reports/etl_report.html`
- **HTML code coverage report:** `reports/coverage/index.html`
- **Execution logs:** `logs/etl_framework.log`

The HTML test report includes the test execution results and the ETL Data Quality Dashboard.

Latest verified local execution results:

- Automated tests passed: 36
- Total code coverage: 95%
- HTML test report generated successfully
- HTML coverage report generated successfully

These figures describe the latest recorded local execution and may change when the code or tests change.

## 13. Continuous Integration

GitHub Actions runs the automated test workflow when changes are pushed to the repository. The workflow prepares its test environment, executes the ETL tests, and uploads the test and coverage reports as downloadable artifacts.

Repository: https://github.com/Sidzzz121/ETL_Testing_Framework

## 14. Future Enhancements

- Testing with larger datasets and performance benchmarks
- Additional data quality rules and transformation scenarios
- More advanced anomaly detection techniques

## 15. Academic Project

This project is developed as an M.Tech project focused on automated ETL testing, data quality assessment, transformation validation, anomaly detection, and continuous integration.
