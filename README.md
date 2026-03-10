# 1 Billion Row Challenge (1BRC) - Python Edition

This project is a Python implementation of the [1 Billion Row Challenge](https://github.com/gunnarmorling/1brc). The goal is to calculate the minimum, mean, and maximum temperature for weather stations from a file containing 1 billion rows of measurements.

## Prerequisites

- Python 3.11+
- `uv` (recommended for dependency management) or `pip`

## Setup

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/digomes87/C1BRC
    cd 1brc
    ```

2.  **Install dependencies**:
    Using `uv` (recommended):

    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

    Or using standard `pip`:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

### 1. Generate Data

You can generate a dataset with 1 billion rows (approx. 13GB).

**Fast Generation (Recommended)**:
Uses multiprocessing and NumPy for high performance (~1.8M rows/s).

```bash
python src/generate_dataset_fast.py --rows 1000000000 --output measurements.txt
```

**Standard Generation**:
Slower, pure Python implementation.

```bash
python src/generate_dataset.py --rows 1000000000 --output measurements.txt
```

### 2. Calculate Statistics

There are multiple implementations available, optimized for different scenarios.

#### A. Polars (Fastest Single Node)

Uses the Polars DataFrame library for extremely fast multi-threaded processing.

```bash
python src/calculate_polars.py measurements.txt
```

#### B. DuckDB (High Performance SQL)

Uses DuckDB's embedded OLAP engine to query the CSV file directly.

```bash
python src/calculate_duckdb.py measurements.txt
```

#### C. Numba (JIT Compiled)

Uses Numba to JIT compile the parsing logic and release the GIL for parallel processing.

```bash
python src/calculate_numba.py measurements.txt
```

#### D. PySpark (Distributed)

Uses Apache Spark for distributed processing. Ideal for clusters or extremely large datasets.

```bash
python src/calculate_spark.py measurements.txt
```

## Performance Benchmarks (1 Million Rows)

| Implementation | Description               | Approximate Time  |
| :------------- | :------------------------ | :---------------- |
| **Polars**     | `src/calculate_polars.py` | ~0.02s            |
| **DuckDB**     | `src/calculate_duckdb.py` | ~0.04s            |
| **Numba**      | `src/calculate_numba.py`  | ~0.15s            |
| **PySpark**    | `src/calculate_spark.py`  | ~4.00s (overhead) |

_Note: For 1 billion rows, Polars and DuckDB are typically the fastest on a single machine._

## Project Structure

- `src/generate_dataset_fast.py`: Optimized data generator.
- `src/generate_dataset.py`: Original data generator.
- `src/calculate_polars.py`: Solution using Polars.
- `src/calculate_duckdb.py`: Solution using DuckDB.
- `src/calculate_numba.py`: Solution using Numba JIT.
- `src/calculate_spark.py`: Solution using PySpark.
- `requirements.txt`: Project dependencies.

# My Conclusion

I am surprised by DuckDB, I didn't expect it to be the champion. There was a cheering for JIT (Numba), which performed well but was easily surpassed by DuckDB.

In the end, it's not about the tool but the application scenario, understanding the business model. Understand that there is no better or worse, and you can even work with more than one resource in the same project.
