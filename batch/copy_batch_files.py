import os
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/opt/airflow/batch/.env")

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

# Create S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Local source folder
SOURCE_FOLDER = "/opt/airflow/batch/source"

# Files to upload
FILES = [
    "train_transaction.csv",
    "train_identity.csv"
]

print("=" * 60)
print("Uploading Batch Files to AWS S3")
print("=" * 60)

for file_name in FILES:

    local_path = os.path.join(SOURCE_FOLDER, file_name)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"{local_path} not found")

    s3_key = f"batch/landing/ieee/{file_name}"

    print(f"Uploading {file_name}...")

    s3.upload_file(
        Filename=local_path,
        Bucket=S3_BUCKET,
        Key=s3_key
    )

    print(f"✓ Uploaded to s3://{S3_BUCKET}/{s3_key}")

print("=" * 60)
print("Batch Upload Completed Successfully")
print("=" * 60)