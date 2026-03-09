import mmap
from os import stat, stat_result
from typing import Dict, List

from ..interfaces.protocols import ChunkProcessor


class OptimizedChunkProcessor(ChunkProcessor):
    """
    Proccesses file chunks using memory mapping and optimized parsing
    """

    def process(self, filename: str, start: int, end: int) -> Dict[str, List[int]]:
        results = {}

        try:
            with open(filename, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    mm.seek(start)
                    current_pos = start

                    while current_pos < end:
                        line_end = mm.find(b"\n", current_pos, end)
                        if line_end == -1:
                            if current_pos < end:
                                line_end = end
                            else:
                                break

                        line = mm[current_pos:line_end]
                        current_pos = line_end + 1

                        sep_index = line.find(b";")
                        if sep_index == -1:
                            continue

                        station = line[:sep_index].decode("utf-8")
                        temp_part = line[sep_index + 1 :]

                        try:
                            dot_pos = temp_part.find(b".")
                            if dot_pos != -1:
                                temp = int(round(float(temp_part) * 10))
                            else:
                                temp = int(temp_part) * 10

                            if station not in results:
                                results[station] = [temp, temp, temp, 1]
                            else:
                                stats = results[station]

                                if temp < stats[0]:
                                    stats[0] = temp

                                stats[2] += temp
                                stats[3] += 1

                        except ValueError:
                            continue

        except Exception as e:
            print(f"Error processing chunk: {e}")
            return {}

        return results


def process_chunk_wrapper(filename: str, start: int, end: int) -> Dict[str, List[int]]:
    processor = OptimizedChunkProcessor()
    return processor.process(filename, start, end)
