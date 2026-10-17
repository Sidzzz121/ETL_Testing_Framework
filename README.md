# Automated ETL Testing Framework

## Project Overview

The Automated ETL Testing Framework is a Python-based project designed to validate data quality and transformation accuracy in an Extract, Transform, Load (ETL) pipeline.

It extracts customer records from a PostgreSQL source table, applies transformation logic, loads the results into a target table, and executes automated validation tests using Pytest.

## Objectives

- Automate ETL data validation.
- Verify source and target row counts.
- Detect null values, duplicates, and invalid email formats.
- Validate database schemas and data types.
- Verify transformation logic.
- Check referential integrity and financial reconciliation.
- Generate HTML test execution reports.

## Technology Stack

- Python
- PostgreSQL
- pgAdmin
- Pytest
- pytest-html
- psycopg2
- python-dotenv
- Git and GitHub

## Project Structure

```text
ETL_Testing_Framework/
├── config/
├── etl/
│   └── load.py
├── framework/
│   ├── db_utils.py
│   ├── logger.py
│   └── validators.py
├── logs/
├── reports/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run_framework.py
```

## Prerequisites

- Python 3.12 or compatible version
- PostgreSQL
- Git
- Required Python packages from `requirements.txt`

## Configuration

Create a `.env` file in the project root with your local PostgreSQL connection settings:

```text
ETL_DB_HOST=localhost
ETL_DB_PORT=5432
ETL_DB_USER=postgres
ETL_DB_PASSWORD=your_local_password
ETL_DB_NAME=etl_testing_db
```

Replace the example password with your own local PostgreSQL password. Never commit `.env` to GitHub.

## Installation

Install the dependencies:

```bash
pip install -r requirements.txt
```

Ensure PostgreSQL is running and the required source and target tables are configured.

## Run the Framework

Execute the ETL pipeline and automated test suite:

```bash
python run_framework.py
```

The runner executes the ETL process first, then runs Pytest and generates an HTML report.

## Test Coverage

The current test suite covers:

- Source and target row-count validation
- Data comparison
- Null-value detection
- Duplicate detection
- Email-format validation
- Schema validation
- Data-type validation
- Transformation validation
- Referential integrity
- Amount reconciliation
- Negative validation scenarios

## Test Report

After execution, open:

```text
reports/etl_report.html
```

The report contains the automated test results.

## Future Enhancements

- GitHub Actions continuous integration
- More comprehensive transformation and data-quality rules
- Improved reporting and execution metrics
- Larger datasets and performance testing
- Data anomaly detection

## Academic Project

This project is being developed as an M.Tech project focused on automated ETL testing, data quality, and transformation validation.
