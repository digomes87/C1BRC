import argparse
import mmap
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from numba import njit, prange

NEWLINE = 10
SEMICOLON = 59
MINUS = 45
PERIOD = 46
ZERO = 48

FNV_OFFSET = np.uint64(14695981039346656037)
FNV_PRIME = np.uint64(1099511628211)


@njit(nogil=True)
def parse_chunk(data):
    """
    Parse a chunk of bytes using Numba.
    Returns a dictionary mapping station names (bytes) to [min, max, sum, count].
    """
    MAX_STATIONS = 12000
    map_size = 32768
    map_keys = np.full(map_size, -1, dtype=np.int64)
    map_vals_idx = np.full(map_size, -1, dtype=np.int32)

    stats = np.zeros((MAX_STATIONS, 4), dtype=np.int64)
    stats[:, 0] = 9999
    stats[:, 1] = -9999

    station_lens = np.zeros(MAX_STATIONS, dtype=np.int32)

    next_idx = 0

    idx = 0
    n = len(data)

    while idx < n:
        semi_pos = idx
        while semi_pos < n and data[semi_pos] != SEMICOLON:
            semi_pos += 1

        if semi_pos == n:
            break

        h = FNV_OFFSET
        for i in range(idx, semi_pos):
            h = (h ^ np.uint64(data[i])) * FNV_PRIME

        temp_start = semi_pos + 1
        temp_val = 0
        sign = 1

        curr = temp_start
        if data[curr] == MINUS:
            sign = -1
            curr += 1

        while data[curr] != PERIOD:
            temp_val = temp_val * 10 + (data[curr] - ZERO)
            curr += 1

        curr += 1
        temp_val = temp_val * 10 + (data[curr] - ZERO)

        temp_val *= sign

        idx = curr + 2

        slot = h & (map_size - 1)
        while True:
            if map_keys[slot] == -1:
                map_keys[slot] = np.int64(h)
                map_vals_idx[slot] = next_idx

                name_len = semi_pos - (
                    idx - (curr + 2) - (semi_pos - (idx - (curr + 2)))
                )
                break
            elif map_keys[slot] == np.int64(h):
                break
            else:
                slot = (slot + 1) & (map_size - 1)

        s_idx = map_vals_idx[slot]

        if s_idx == next_idx:
            pass

    return None


@njit(nogil=True)
def process_chunk_numba(data):
    CAPACITY = 1000000
    hashes = np.zeros(CAPACITY, dtype=np.int64)
    mins = np.full(CAPACITY, 10000, dtype=np.int32)
    maxs = np.full(CAPACITY, -10000, dtype=np.int32)
    sums = np.zeros(CAPACITY, dtype=np.int64)
    counts = np.zeros(CAPACITY, dtype=np.int32)

    MAP_SIZE = 32768
    map_keys = np.full(MAP_SIZE, -1, dtype=np.int64)
    map_vals = np.full(MAP_SIZE, -1, dtype=np.int32)

    next_id = 0

    i = 0
    n = len(data)

    while i < n:
        h = FNV_OFFSET

        while i < n and data[i] != SEMICOLON:
            h = (h ^ np.uint64(data[i])) * FNV_PRIME
            i += 1

        if i >= n:
            break

        i += 1

        sign = 1
        if data[i] == MINUS:
            sign = -1
            i += 1

        temp = 0
        while data[i] != PERIOD:
            temp = temp * 10 + (data[i] - 48)
            i += 1

        i += 1
        temp = temp * 10 + (data[i] - 48)
        temp *= sign

        i += 2

        slot = h & (MAP_SIZE - 1)
        found_idx = -1

        while True:
            key = map_keys[slot]
            if key == -1:
                map_keys[slot] = np.int64(h)
                map_vals[slot] = next_id
                found_idx = next_id
                hashes[found_idx] = np.int64(h)
                next_id += 1
                break
            elif key == np.int64(h):
                found_idx = map_vals[slot]
                break
            else:
                slot = (slot + 1) & (MAP_SIZE - 1)

        if temp < mins[found_idx]:
            mins[found_idx] = temp
        if temp > maxs[found_idx]:
            maxs[found_idx] = temp
        sums[found_idx] += temp
        counts[found_idx] += 1

    return (
        hashes[:next_id],
        mins[:next_id],
        maxs[:next_id],
        sums[:next_id],
        counts[:next_id],
    )


def get_file_chunks(filename, num_chunks):
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_chunks

    chunks = []
    with open(filename, "rb") as f:
        start = 0
        for i in range(num_chunks):
            end = start + chunk_size
            if i == num_chunks - 1:
                end = file_size
            else:
                f.seek(end)
                f.readline()
                end = f.tell()

            chunks.append((filename, start, end))
            start = end

    return chunks


def process_wrapper(args):
    filename, start, end = args
    with open(filename, "rb") as f:
        f.seek(start)
        data = f.read(end - start)

    data_arr = np.frombuffer(data, dtype=np.uint8)
    return process_chunk_numba(data_arr)


def calculate(filename):
    print(f"Processing {filename} with Numba...")
    start_time = time.time()

    num_cores = os.cpu_count()
    chunks = get_file_chunks(filename, num_cores)

    results = []
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        for res in executor.map(process_wrapper, chunks):
            results.append(res)

    print("Aggregation complete (names skipped for Numba demo simplicity).")

    final_stats = {}

    for hashes, mins, maxs, sums, counts in results:
        for i in range(len(hashes)):
            h = hashes[i]
            if h not in final_stats:
                final_stats[h] = [mins[i], maxs[i], sums[i], counts[i]]
            else:
                s = final_stats[h]
                s[0] = min(s[0], mins[i])
                s[1] = max(s[1], maxs[i])
                s[2] += sums[i]
                s[3] += counts[i]

    end_time = time.time()
    print(
        f"Processed {len(final_stats)} unique stations in {end_time - start_time:.2f} seconds"
    )
    print(
        "Note: Numba implementation here is a proof-of-concept for the calculation kernel."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1BRC with Numba")
    parser.add_argument("filename", nargs="?", default="measurements.txt")
    args = parser.parse_args()

    calculate(args.filename)
