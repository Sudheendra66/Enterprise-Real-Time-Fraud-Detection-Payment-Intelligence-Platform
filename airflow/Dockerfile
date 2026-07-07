FROM apache/airflow:2.10.0

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==2.10.0" \
    "apache-airflow-providers-databricks<=6" \
    "databricks-sdk" \
    "boto3"

# dbt-core 1.11+ requires protobuf>=6.0 which conflicts with Airflow's opentelemetry-proto.
# Install dbt separately allowing protobuf/opentelemetry upgrades.
# Patch dbt's click._OptionParser import for compatibility with click 8.1.7
RUN pip install --no-cache-dir "click<8.2" "dbt-core==1.11.0" "dbt-databricks==1.11.0" && \
    python -c "p='/home/airflow/.local/lib/python3.12/site-packages/dbt/cli/options.py';c=open(p).read().replace('from click.parser import _OptionParser, _ParsingState','from click.parser import OptionParser as _OptionParser, ParsingState as _ParsingState');open(p,'w').write(c);print('Patched')"