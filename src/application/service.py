import multiprocessing
import time

from ..interfaces import (
    ChunkProcessor,
    DataReader,
    ResultAggregator,
    ResultFormatter,
)


class WeatherAnalyzer:
    """
    Orchestrates the process of reading , processing, agregation, and formatting data
    """

    def __init__(
        self,
        reader: DataReader,
        processor: ChunkProcessor,
        aggregator: ResultAggregator,
        formatter: ResultFormatter,
    ) -> None:
        self.reader = reader
        self.processor = processor
        self.aggregator = aggregator
        self.formatter = formatter

    def analyze(self, filename: str) -> str:
        """
        Run the analysis on the given file and return the formatted result
        """
        print(f"Analyzing {filename}....")
        start_time = time.time()

        try:
            chunks = self.reader.read_chunks(filename)
        except Exception as e:
            return f"Error reading file: {e}"

        if not chunks:
            return "{}"

        num_processes = len(chunks)
        print(f"Processing with {num_processes} chuncks/processing")

        from ..infrastructure import process_chunk_wrapper

        with multiprocessing.Pool(processes=num_processes) as pool:
            args = [(filename, start, end) for start, end in chunks]
            partial_results = pool.starmap(process_chunk_wrapper, args)

        final_results = self.aggregator.aggregate(partial_results)
        output = self.formatter.format(final_results)

        end_time = time.time()
        print(f"Processing in {end_time - start_time:.2f} seconds")

        return output
