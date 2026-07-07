import os
from dotenv import load_dotenv
import boto3

load_dotenv("/opt/airflow/batch/.env")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

bucket = os.getenv("S3_BUCKET")

source_folder = "/opt/airflow/batch/source"

files = [
    "train_transaction.csv",
    "train_identity.csv"
]

for file in files:

    local_file = os.path.join(source_folder, file)

    s3.upload_file(
        local_file,
        bucket,
        f"batch/landing/ieee/{file}"
    )

    print(f"Uploaded {file}")

print("Upload completed.")