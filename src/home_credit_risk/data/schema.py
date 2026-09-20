import pandera.pandas as pa

application_train_schema = pa.DataFrameSchema(
    columns={
        "SK_ID_CURR": pa.Column(
            int, unique=True, nullable=False
        ),  # must be unique non-null
        "TARGET": pa.Column(int, pa.Check.isin([0, 1]), nullable=False),
        "AMT_INCOME_TOTAL": pa.Column(
            float, pa.Check.ge(0), nullable=True
        ),  # non-negative
    },
    strict=False,
)
