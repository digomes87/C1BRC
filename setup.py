from setuptools import find_packages, setup

setup(
    name="1brc-python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tqdm",
        "polars",
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "1brc-calculate=src.calculate:main",
            "1brc-generate=src.generate_dataset:main",
        ],
    },
)
