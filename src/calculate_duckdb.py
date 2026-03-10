import argparse
import time

import duckdb


def calculate(filename):
    print(f"Processing {filename} with DuckDB...")
    start_time = time.time()
    con = duckdb.connect(database=":memory:")

    query = f"""
        SELECT 
            column0 as station, 
            min(column1) as min_temp,
            avg(column1) as mean_temp,
            max(column1) as max_temp
        FROM read_csv('{filename}', delim=';', header=False, columns={{'column0': 'VARCHAR', 'column1': 'DOUBLE'}})
        GROUP BY station
        ORDER BY station
    """

    result = con.execute(query).fetchall()
    end_time = time.time()

    output_parts = []
    for row in result:
        station, min_t, mean_t, max_t = row
        output_parts.append(f"{station}={min_t:.1f}/{mean_t:.1f}/{max_t:.1f}")

    print(f"{{{', '.join(output_parts)}}}")
    print(f"\nProcessed in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1BRC with DuckDB")
    parser.add_argument("filename", nargs="?", default="measurements.txt")
    args = parser.parse_args()

    calculate(args.filename)
