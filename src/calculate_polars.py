import argparse
import time

import polars as pl


def calculate(filename):
    print(f"Processing {filename} with Polars...")
    start_time = time.time()
    q = (
        pl.scan_csv(
            filename,
            separator=";",
            has_header=False,
            new_columns=["station", "measure"],
            schema={"station": pl.String, "measure": pl.Float64},
        )
        .group_by("station")
        .agg(
            [
                pl.min("measure").alias("min"),
                pl.mean("measure").alias("mean"),
                pl.max("measure").alias("max"),
            ]
        )
        .sort("station")
    )

    df = q.collect()

    end_time = time.time()

    result_str = ", ".join(
        f"{row['station']}={row['min']:.1f}/{row['mean']:.1f}/{row['max']:.1f}"
        for row in df.iter_rows(named=True)
    )
    print(f"{{{result_str}}}")
    print(f"\nProcessed in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1BRC with Polars")
    parser.add_argument("filename", nargs="?", default="measurements.txt")
    args = parser.parse_args()

    calculate(args.filename)
