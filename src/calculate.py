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
