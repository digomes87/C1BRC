from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class DataReader(ABC):
    @abstractmethod
    def read_chunks(self, filename: str) -> List[Tuple[int, int]]:
        pass


class ChunkProcessor(ABC):
    @abstractmethod
    def process(self, filename: str, strt: int, end: int) -> Dict[str, Any]:
        pass


class ResultAggregator(ABC):
    @abstractmethod
    def aggregate(self, partial_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass


class ResultFormatter(ABC):
    @abstractmethod
    def format(self, results: Dict[str, Any]) -> str:
        pass
