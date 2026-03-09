import os
from typing import List, Tuple

from ..interfaces.protocols import DataReader


class MmapChunker(DataReader):
    """
    Implements file chunking using file size and seek operations
    """

    def __init__(self, num_chunks: int):
        self.num_chunks = num_chunks

    def read_chunks(self, filename: str) -> List[Tuple[int, int]]:
        """
        Split a file into roughly  equal chunks, aligning to newline characters
        returns a lista of start end byte offsets
        """

        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")

        file_size = os.path.getsize(filename)
        if file_size == 0:
            return []

        if file_size < 1000:
            return [(0, file_size)]

        chunck_size = file_size // self.num_chunks
        chunks = []

        with open(filename, "rb") as f:
            start = 0

            for i in range(self.num_chunks):
                if i == self.num_chunks - 1:
                    end = file_size
                    chunks.append((start, end))
                    break

                f.seek(start + chunck_size)
                f.readline()
                end = f.tell()

                chunks.append((start, end))
                start = end

        return chunks
