import argparse
import random
import time
from typing import List, Tuple

from tqdm import tqdm


class DatasetGenerator:
    """
    Generates synthetic dataset for 1 billion row challenge
    """

    def __init__(self, num_stations: int = 10000):
        self.num_stations = num_stations
        self.stations: List[Tuple[str, float]] = []
        self._initialize_stations()

    def _initialize_stations(self):
        """Generate a list of station names with their name temperature"""
        for i in range(self.num_stations):
            name = f"Station_{i}"
            mean_temp = random.uniform(-20, 40)
            self.stations.append((name, mean_temp))

    def generate(self, filename: str, num_rows: int):
        """Generate the measurements file"""
        print(f"Generating {num_rows} measurements for {self.num_stations} stations")
        start_time = time.time()

        buffer_size = 100_000
        buffer = []

        with open(filename, "w", encoding="utf-8") as f:
            for _ in tqdm(range(num_rows), unit="rows"):
                station, mean_temp = random.choice(self.stations)
                temp = random.gauss(mean_temp, 10)
                line = f"{station};{temp:.1f}\n"
                buffer.append(line)

                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer = []

            if buffer:
                f.writelines(buffer)

        end_time = time.time()
        print(
            f"Generated {num_rows} measurements in {end_time - start_time:.2f} seconds"
        )
        print(f"File saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Generate 1BRC dataset")
    parser.add_argument(
        "--rows", type=int, default=1_000_000_000, help="Number of rows to generate"
    )
    parser.add_argument(
        "--stations", type=int, default=10000, help="Number of unique station"
    )
    parser.add_argument(
        "--output", type=str, default="measurements.txt", help="Output filename"
    )

    args = parser.parse_args()

    generator = DatasetGenerator(num_stations=args.stations)
    generator.generate(args.output, args.rows)


if __name__ == "__main__":
    main()
