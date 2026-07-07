from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="master_pipeline",
    description="Top-level placeholder DAG for fraud platform orchestration readiness checks.",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["fraud-platform", "orchestration"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end
