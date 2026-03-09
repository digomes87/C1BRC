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
    def __init__(self, filename: str):
        self.filename = filename

    def execute(self):
        if not os.path.exists(self.filename):
            print(f"File {self.filename} not found")
            return

        num_chunks = multiprocessing.cpu_count()

        reader = MmapChunker(num_chunks)
        processor = OptimizedChunkProcessor()
        aggregator = ParallellAggregator()
        formatter = DefaultFormatter()

        analyzer = WeatherAnalyzer(reader, processor, aggregator, formatter)

        result = analyzer.analyze(self.filename)
        print(result)


def main():
    if len(sys.argv) < 2:
        filename = "measurements.txt"
    else:
        filename = sys.argv[1]

    service = WeatherStationService(filename)
    service.execute()


if __name__ == "__main__":
    main()
