import os

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from src.utils.spark_session import create_spark_session


def main():

    spark = create_spark_session("KafkaToBronze")

    schema = StructType(
        [
            StructField("TransactionID", IntegerType()),
            StructField("isFraud", IntegerType()),
            StructField("TransactionDT", IntegerType()),
            StructField("TransactionAmt", DoubleType()),
            StructField("ProductCD", StringType()),
            StructField("card4", StringType()),
            StructField("card6", StringType()),
            StructField("addr1", DoubleType()),
            StructField("addr2", DoubleType()),
            StructField("P_emaildomain", StringType()),
            StructField("R_emaildomain", StringType()),
        ]
    )

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "fraud.transactions.raw")
        .option("startingOffsets", "earliest")
        .load()
    )

    # Parse JSON value from Kafka
    parsed = (
        df.selectExpr("CAST(value AS STRING) as json_value")
        .select(from_json(col("json_value"), schema).alias("data"))
        .select("data.*")
    )

    bronze_path = os.path.join(
        os.getcwd(),
        "data",
        "bronze",
    )

    checkpoint_path = os.path.join(
        os.getcwd(),
        "data",
        "checkpoints",
        "bronze",
    )

    # Ensure directories exist before starting stream
    os.makedirs(bronze_path, exist_ok=True)
    os.makedirs(checkpoint_path, exist_ok=True)

    # Start the Delta write stream
    query = (
        parsed.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .start(bronze_path)
    )

    print("=" * 60)
    print("Streaming Started")
    print("=" * 60)
    print("Kafka Topic :", "fraud.transactions.raw")
    print("Bronze Path :", bronze_path)
    print("Checkpoint  :", checkpoint_path)
    print("=" * 60)

    query.awaitTermination()


if __name__ == "__main__":
    main()