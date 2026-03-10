import argparse
import multiprocessing
import os
import random
import time

import numpy as np
from tqdm import tqdm


def generate_chunk(args):
    """
    Generate a chunk of data.
    """
    num_rows, stations = args
    rng = np.random.default_rng()
    station_indices = rng.integers(0, len(stations), size=num_rows)
    station_means = np.array([s[1] for s in stations])
    selected_means = station_means[station_indices]
    temps = rng.normal(selected_means, 10.0)
    station_names = [stations[i][0] for i in station_indices]
    lines = [f"{name};{temp:.1f}\n" for name, temp in zip(station_names, temps)]

    return lines


def write_chunk(filename, lines, mode="a"):
    with open(filename, mode, encoding="utf-8") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate 1BRC dataset optimized")
    parser.add_argument(
        "--rows", type=int, default=1_000_000_000, help="Number of rows to generate"
    )
    parser.add_argument(
        "--stations", type=int, default=10_000, help="Number of unique stations"
    )
    parser.add_argument(
        "--output", type=str, default="measurements.txt", help="Output filename"
    )
    parser.add_argument(
        "--cores", type=int, default=os.cpu_count(), help="Number of cores to use"
    )

    args = parser.parse_args()

    print(f"Generating {args.rows:,} measurements using {args.cores} cores...")
    start_time = time.time()

    station_names = [f"Station_{i}" for i in range(args.stations)]
    station_means = [random.uniform(-20, 40) for _ in range(args.stations)]
    stations = list(zip(station_names, station_means))

    chunk_size = args.rows // args.cores
    remainder = args.rows % args.cores

    tasks = []
    for i in range(args.cores):
        rows = chunk_size + (1 if i < remainder else 0)
        tasks.append((rows, stations, i))

    BATCH_SIZE = 1_000_000
    total_batches = (args.rows + BATCH_SIZE - 1) // BATCH_SIZE

    with open(args.output, "w") as f:
        pass

    print(f"Total batches {total_batches}")

    pool = multiprocessing.Pool(processes=args.cores)

    batch_tasks = []
    rows_generated = 0
    while rows_generated < args.rows:
        current_batch = min(BATCH_SIZE, args.rows - rows_generated)
        batch_tasks.append((current_batch, stations, rows_generated))
        rows_generated += current_batch

    print(f"Processing {len(batch_tasks)} batches...")

    with open(args.output, "a", encoding="utf-8") as f:
        for lines in tqdm(
            pool.imap_unordered(generate_chunk, batch_tasks), total=len(batch_tasks)
        ):
            f.writelines(lines)

    pool.close()
    pool.join()

    end_time = time.time()
    size_mb = os.path.getsize(args.output) / (1024 * 1024)
    print(f"Done in {end_time - start_time:.2f}s")
    print(f"Throughput: {args.rows / (end_time - start_time):,.0f} rows/s")
    print(f"File size: {size_mb:,.2f} MB")


if __name__ == "__main__":
    main()
