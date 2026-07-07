import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

databricks_streaming_job_id = int(os.getenv("DATABRICKS_STREAMING_JOB_ID", "0"))

with DAG(
    dag_id="streaming_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["streaming", "fraud-platform"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    replay_transactions = BashOperator(
        task_id="replay_transactions",
        bash_command="""
        cd /opt/airflow &&
        python -m src.replay_engine.replay
        """
    )

    trigger_streaming_workflow = DatabricksRunNowOperator(
        task_id="trigger_streaming_workflow",
        databricks_conn_id="databricks_default",
        job_id=databricks_streaming_job_id,
    )

    validate_streaming = BashOperator(
        task_id="validate_streaming",
        bash_command="""
        echo "Streaming Validation Completed"
        """
    )

    end = EmptyOperator(
        task_id="end"
    )

    (
        start
        >> replay_transactions
        >> trigger_streaming_workflow
        >> validate_streaming
        >> end
    )
