import argparse
import os
import random
import time
from typing import List, Tuple

from tqdm import tqdm


class DatasetGenerator:
    """Generates synthetic dataset for the 1 billion row challenge."""

    __slots__ = ("num_stations", "stations")

    def __init__(self, num_stations: int = 10_000) -> None:
        self.num_stations = num_stations
        self.stations: List[Tuple[str, float]] = [
            (f"Station_{i}", random.uniform(-20, 40)) for i in range(num_stations)
        ]

    def generate(
        self, filename: str, num_rows: int, buffer_size: int = 1_000_000
    ) -> None:
        """Generate the measurements file."""
        print(
            f"Generating {num_rows:,} measurements for {self.num_stations:,} stations"
        )
        start = time.perf_counter()

        stations = self.stations
        gauss = random.gauss
        choice = random.choice

        with open(filename, "w", encoding="utf-8", buffering=8 * 1024 * 1024) as f:
            buffer: List[str] = []
            append = buffer.append

            for _ in tqdm(range(num_rows), unit="rows", unit_scale=True):
                station, mean_temp = choice(stations)
                append(f"{station};{gauss(mean_temp, 10):.1f}\n")

                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer.clear()

            if buffer:
                f.writelines(buffer)

        elapsed = time.perf_counter() - start
        size_mb = os.path.getsize(filename) / 1024 / 1024
        print(
            f"Done in {elapsed:.2f}s — {num_rows / elapsed:,.0f} rows/s — {size_mb:,.1f} MB saved to {filename}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 1BRC dataset")
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
        "--buffer", type=int, default=1_000_000, help="Write buffer size (rows)"
    )
    args = parser.parse_args()

    DatasetGenerator(num_stations=args.stations).generate(
        args.output, args.rows, args.buffer
    )


if __name__ == "__main__":
    main()
