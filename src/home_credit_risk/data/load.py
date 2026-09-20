from pathlib import Path

import duckdb

from home_credit_risk.data.schema import application_train_schema

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/home_credit.duckdb")

TABLES = [
    "application_train",
    "application_test",
    "bureau",
    "bureau_balance",
    "previous_application",
    "POS_CASH_balance",
    "installments_payments",
    "credit_card_balance",
]


def load_raw_to_duckdb(con: duckdb.DuckDBPyConnection) -> None:
    for table in TABLES:
        csv_path = RAW_DIR / f"{table}.csv"
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Loaded {table}: {count:,} rows")


def validate_application_train(con: duckdb.DuckDBPyConnection) -> None:
    """
    Validates schema for training dataset.
    """
    df = con.execute("SELECT * FROM application_train").df()
    application_train_schema.validate(df)
    print("application_train schema OK")


if __name__ == "__main__":
    con = duckdb.connect(str(DB_PATH))
    load_raw_to_duckdb(con)
    validate_application_train(con)
    con.close()
