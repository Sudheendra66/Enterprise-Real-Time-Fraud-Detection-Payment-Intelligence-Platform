import os

from pyspark.sql import SparkSession


def create_spark_session(app_name="FraudDetectionStreaming"):

    spark_master = os.getenv("SPARK_MASTER", "local[*]")

    # -----------------------------
    # Package Dependencies
    # -----------------------------
    packages = [
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4",
        "io.delta:delta-spark_2.12:3.2.1",
    ]

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(spark_master)
        .config(
            "spark.jars.packages",
            ",".join(packages),
        )

        # -----------------------------
        # Delta Lake Configuration
        # -----------------------------
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )

        # -----------------------------
        # Windows Compatibility
        # -----------------------------
        # Point to hadoop native libraries
        .config("spark.driver.extraLibraryPath", "C:\\hadoop\\bin")
        .config("spark.executor.extraLibraryPath", "C:\\hadoop\\bin")
    )

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    return spark