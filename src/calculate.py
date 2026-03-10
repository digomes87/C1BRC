import multiprocessing
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.application import DefaultFormatter, WeatherAnalyzer
from src.infrastructure import (
    MmapChunker,
    OptimizedChunkProcessor,
    ParallellAggregator,
)


class WeatherStationService:
    __slots__ = ("filename",)

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def execute(self) -> None:
        if not os.path.exists(self.filename):
            print(f"File {self.filename} not found", file=sys.stderr)
            return

        num_chunks = multiprocessing.cpu_count()

        result = WeatherAnalyzer(
            MmapChunker(num_chunks),
            OptimizedChunkProcessor(),
            ParallellAggregator(),
            DefaultFormatter(),
        ).analyze(self.filename)

        print(result)


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "measurements.txt"
    WeatherStationService(filename).execute()


if __name__ == "__main__":
    main()
