import duckdb

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
