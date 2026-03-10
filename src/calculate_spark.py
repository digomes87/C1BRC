import argparse
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import max, mean, min


def calculate(filename):
    print("Starting Spark Session...")
    spark = (
        SparkSession.builder.appName("1BRC")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .getOrCreate()
    )

    print(f"Processing {filename} with PySpark...")
    start_time = time.time()
    schema = "station STRING, temperature DOUBLE"

    df = spark.read.csv(filename, sep=";", schema=schema, header=False)

    result = (
        df.groupBy("station")
        .agg(
            min("temperature").alias("min"),
            mean("temperature").alias("mean"),
            max("temperature").alias("max"),
        )
        .orderBy("station")
    )

    rows = result.collect()
    end_time = time.time()

    output_parts = []
    for row in rows:
        output_parts.append(
            f"{row['station']}={row['min']:.1f}/{row['mean']:.1f}/{row['max']:.1f}"
        )

    print(f"{{{', '.join(output_parts)}}}")
    print(f"\nProcessed in {end_time - start_time:.2f} seconds")

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1BRC with PySpark")
    parser.add_argument("filename", nargs="?", default="measurements.txt")
    args = parser.parse_args()

    calculate(args.filename)
