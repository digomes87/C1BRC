# 1 Billion Row Challenge (1BRC) - Python Implementation

This project is a high-performance Python implementation of the [One Billion Row Challenge](https://github.com/gunnarmorling/1brc). The goal is to process a massive text file containing temperature measurements for various weather stations and calculate the minimum, mean, and maximum temperature for each station as fast as possible.

## Features

-   **High Performance**: Utilizes `multiprocessing` for parallel execution and `mmap` for efficient file I/O.
-   **Data Generation**: Includes a tool to generate synthetic datasets of arbitrary sizes.
-   **Validation**: Comes with a baseline validator to ensure the correctness of the optimized implementation.
-   **Modular Architecture**: Clean separation of concerns using Domain-Driven Design (DDD) principles.

## Prerequisites

-   Python 3.11 or higher
-   [`uv`](https://github.com/astral-sh/uv) (Recommended for fast package management) or `pip`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd 1brc
    ```

2.  **Set up the environment**:
    We recommend using `uv` for a faster and more reliable setup.

    ```bash
    # Create a virtual environment
    uv venv .venv

    # Activate the environment
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    # Install dependencies
    uv pip install -r requirements.txt
    ```

## Usage

### 1. Generate the Dataset
Before running the challenge, you need to generate the measurements file. You can specify the number of rows (default is 1 billion).

```bash
# Generate 1 billion rows (standard challenge)
python src/generate_dataset.py --rows 1000000000 --output measurements.txt

# Generate a smaller dataset for testing (e.g., 1 million rows)
python src/generate_dataset.py --rows 1000000 --output measurements.txt
```

**Arguments:**
-   `--rows`: Number of rows to generate (default: 1,000,000,000)
-   `--stations`: Number of unique weather stations (default: 10,000)
-   `--output`: Output filename (default: `measurements.txt`)

### 2. Run the Calculation
Execute the main processing script to calculate the statistics.

```bash
python src/calculate.py measurements.txt
```

If no filename is provided, it defaults to `measurements.txt`.

### 3. Validate Results
To verify the correctness of the optimized implementation, you can run the baseline validator. This is useful for checking smaller datasets.

```bash
python src/validate.py measurements.txt
```

## Project Structure

```
1brc/
├── src/
│   ├── application/        # Application logic and orchestration
│   ├── domain/             # Domain models
│   ├── infrastructure/     # Low-level implementation (File I/O, Processing)
│   ├── interfaces/         # Protocols and Interfaces
│   ├── calculate.py        # Main entry point for the challenge
│   ├── generate_dataset.py # Dataset generation script
│   └── validate.py         # Baseline validation script
├── measurements.txt        # Generated data file (not committed)
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## How It Works

1.  **Chunking**: The input file is split into chunks based on the number of available CPU cores.
2.  **Memory Mapping**: Each worker process uses `mmap` to read its assigned chunk efficiently without loading the entire file into memory.
3.  **Parallel Processing**: Workers parse lines and aggregate temperature data (min, max, sum, count) locally.
4.  **Aggregation**: Partial results from all workers are merged into a final result set.
5.  **Formatting**: The final statistics are formatted and printed to standard output.
