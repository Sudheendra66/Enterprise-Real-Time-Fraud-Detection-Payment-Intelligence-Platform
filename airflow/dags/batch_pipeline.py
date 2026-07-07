import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

databricks_batch_job_id = int(os.getenv("DATABRICKS_BATCH_JOB_ID", "0"))

# -------------------------------------------------
# DEFAULT ARGUMENTS
# -------------------------------------------------

default_args = {
    "owner": "Dileep",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# -------------------------------------------------
# DAG
# -------------------------------------------------

with DAG(
    dag_id="batch_pipeline",
    description="Enterprise Fraud Detection Batch Pipeline using Airflow, AWS S3, Databricks and dbt",
    default_args=default_args,
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=[
        "fraud",
        "aws",
        "s3",
        "databricks",
        "dbt",
        "batch",
        "production"
    ],
    doc_md="""
# Enterprise Fraud Detection Platform

## Pipeline Flow

1. Upload batch files to AWS S3
2. Validate uploaded files
3. Trigger Databricks Workflow
4. Build Gold Layer using dbt
5. Create dbt Snapshots
6. Generate dbt Documentation

Owner: Dileep Kumar
""",
) as dag:

    # -------------------------------------------------
    # START
    # -------------------------------------------------

    start = EmptyOperator(
        task_id="start"
    )

    # -------------------------------------------------
    # UPLOAD FILES TO S3
    # -------------------------------------------------

    upload_batch_files_to_s3 = BashOperator(
        task_id="upload_batch_files_to_s3",
        execution_timeout=timedelta(minutes=20),
        bash_command="""
        echo "Uploading batch files to S3..."

        cd /opt/airflow

        python batch/copy_batch_files.py

        echo "Batch upload completed."
        """
    )

    # -------------------------------------------------
    # VALIDATE FILES
    # -------------------------------------------------

    validate_uploaded_files = BashOperator(
        task_id="validate_uploaded_files",
        execution_timeout=timedelta(minutes=10),
        bash_command="""
        echo "Validating uploaded files..."

        cd /opt/airflow

        python batch/validate_s3.py

        echo "Validation completed."
        """
    )

    # -------------------------------------------------
    # RUN DATABRICKS WORKFLOW
    # -------------------------------------------------

    run_databricks_batch_workflow = DatabricksRunNowOperator(
        task_id="run_databricks_batch_workflow",
        databricks_conn_id="databricks_default",
        job_id=databricks_batch_job_id,
        polling_period_seconds=30,
        wait_for_termination=True,
        execution_timeout=timedelta(hours=1),
    )

    # -------------------------------------------------
    # DBT BUILD
    # -------------------------------------------------

    run_dbt_build = BashOperator(
        task_id="run_dbt_build",
        execution_timeout=timedelta(minutes=30),
        bash_command="""
        echo "Starting dbt Build..."

        cd /opt/airflow/dbt/fraud_gold

        dbt build --profiles-dir /opt/airflow/dbt/profiles

        echo "dbt Build completed."
        """
    )

    # -------------------------------------------------
    # DBT SNAPSHOT
    # -------------------------------------------------

    run_dbt_snapshot = BashOperator(
        task_id="run_dbt_snapshot",
        execution_timeout=timedelta(minutes=20),
        bash_command="""
        echo "Creating dbt Snapshots..."

        cd /opt/airflow/dbt/fraud_gold

        dbt snapshot --profiles-dir /opt/airflow/dbt/profiles

        echo "dbt Snapshot completed."
        """
    )

    # -------------------------------------------------
    # DBT DOCS
    # -------------------------------------------------

    generate_dbt_docs = BashOperator(
        task_id="generate_dbt_docs",
        execution_timeout=timedelta(minutes=20),
        bash_command="""
        echo "Generating dbt Documentation..."

        cd /opt/airflow/dbt/fraud_gold

        dbt docs generate --profiles-dir /opt/airflow/dbt/profiles

        echo "dbt Documentation generated."
        """
    )

    # -------------------------------------------------
    # END
    # -------------------------------------------------

    end = EmptyOperator(
        task_id="end"
    )

    # -------------------------------------------------
    # PIPELINE
    # -------------------------------------------------

    (
        start
        >> upload_batch_files_to_s3
        >> validate_uploaded_files
        >> run_databricks_batch_workflow
        >> run_dbt_build
        >> run_dbt_snapshot
        >> generate_dbt_docs
        >> end
    )
