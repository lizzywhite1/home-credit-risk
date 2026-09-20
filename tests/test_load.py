import duckdb
import pandera.errors
import pytest

from home_credit_risk.data.schema import application_train_schema


def test_application_train_schema_on_fixture():
    """
    Unit test to check that synthetic application training data follows schema.
    """
    con = duckdb.connect()
    con.execute("""
        CREATE TABLE application_train AS
        SELECT * FROM read_csv_auto('tests/fixtures/application_train_sample.csv')
    """)
    df = con.execute("SELECT * FROM application_train").df()

    application_train_schema.validate(df)


def test_application_train_schema_rejects_bad_target():
    """
    Target is out of range
    """
    con = duckdb.connect()
    con.execute("""
        CREATE TABLE bad_data AS
        SELECT * FROM (VALUES (100001, 2, 180000.0))
        AS t(SK_ID_CURR, TARGET, AMT_INCOME_TOTAL)
    """)
    df = con.execute("SELECT * FROM bad_data").df()

    with pytest.raises(pandera.errors.SchemaError):
        application_train_schema.validate(df)
