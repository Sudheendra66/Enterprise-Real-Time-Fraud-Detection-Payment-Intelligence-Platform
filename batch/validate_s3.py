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

required = [
    "batch/landing/ieee/train_transaction.csv",
    "batch/landing/ieee/train_identity.csv"
]

for obj in required:

    s3.head_object(
        Bucket=bucket,
        Key=obj
    )

    print(f"{obj} exists")

print("Validation Successful")