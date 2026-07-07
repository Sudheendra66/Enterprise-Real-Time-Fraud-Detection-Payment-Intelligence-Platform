import os
import sys

LANDING = "batch/landing/ieee" 

required_files = [
    "train_transaction.csv",
    "train_identity.csv"
]

for file in required_files:

    path = os.path.join(LANDING, file)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{file} not found.")

    if os.path.getsize(path) == 0:
        raise Exception(f"{file} is empty.")

print("Landing validation successful.")