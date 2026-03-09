import mmap
from typing import Any, Dict, List

from ..interfaces.protocols import ChunkProcessor


class OptimizedChunkProcessor(ChunkProcessor):
    """
    Processes file chunks using memory mapping and optimized parsing.
    """

    def _parse_temp(self, temp_part: bytes) -> int:
        """
        Parses temperature bytes to int (multiplied by 10).
        """
        dot_pos = temp_part.find(b".")
        if dot_pos != -1:
            # Using float trick: round(float(str) * 10)
            return int(round(float(temp_part) * 10))
        else:
            return int(temp_part) * 10

    def _update_stats(
        self, results: Dict[str, List[int]], station: str, temp: int
    ) -> None:
        """
        Updates statistics for a station.
        """
        if station not in results:
            # [min, max, sum, count]
            results[station] = [temp, temp, temp, 1]
        else:
            stats = results[station]
            if temp < stats[0]:
                stats[0] = temp
            if temp > stats[1]:
                stats[1] = temp
            stats[2] += temp
            stats[3] += 1

    def process(self, filename: str, start: int, end: int) -> Dict[str, Any]:
        """
        Process a chunk of the file and return partial results.
        Returns a raw dictionary {station: [min, max, sum, count]} for performance.
        """
        results = {}

        try:
            with open(filename, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    mm.seek(start)
                    current_pos = start

                    while current_pos < end:
                        # Find end of line
                        line_end = mm.find(b"\n", current_pos, end)
                        if line_end == -1:
                            line_end = end if current_pos < end else -1
                            if line_end == -1:
                                break

                        line = mm[current_pos:line_end]
                        current_pos = line_end + 1

                        sep_index = line.find(b";")
                        if sep_index == -1:
                            continue

                        station = line[:sep_index].decode("utf-8")
                        temp_part = line[sep_index + 1 :]

                        try:
                            temp = self._parse_temp(temp_part)
                            self._update_stats(results, station, temp)
                        except ValueError:
                            continue

        except Exception as e:
            print(f"Error processing chunk: {e}")
            return {}

        return results


def process_chunk_wrapper(filename: str, start: int, end: int) -> Dict[str, List[int]]:
    """
    Wrapper function for multiprocessing serialization.
    """
    processor = OptimizedChunkProcessor()
    return processor.process(filename, start, end)
