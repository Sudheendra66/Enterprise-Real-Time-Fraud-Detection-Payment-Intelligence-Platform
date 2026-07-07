# fraud_gold dbt Project

This dbt project defines curated gold-layer fraud analytics models for the Enterprise Real-Time Fraud Detection Platform.

## Contents

- `models/staging/stg_transactions.sql` standardizes scored transaction input.
- `models/gold/` contains fraud, risk, payment method, customer, merchant, amount bucket, and trend summaries.
- `snapshots/` contains customer risk snapshot logic.
- `tests/` contains project-level quality checks.
- `macros/` contains reusable fraud metric SQL helpers.

## Validation

```bash
dbt deps
dbt parse
dbt compile
dbt test
```

Use an external dbt profile. Do not commit profiles containing Databricks hostnames, tokens, or warehouse IDs.

## CI Behavior

GitHub Actions validates `dbt deps`, `dbt parse`, and `dbt compile` with a temporary local DuckDB profile. CI does not execute `dbt run` and does not require cloud credentials.
