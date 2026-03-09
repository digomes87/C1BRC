import sys
from typing import Dict, List, Optional


class BaselineValidator:
    """
    Validates the 1brc results usind a simgple implementation
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.results: Dict[str, List[float]] = {}

    def calculate(self) -> Dict[str, List[float]]:
        """
        Reads line by line simple processings and returns a dic of raw stats
        """

        self.results = {}

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(";")
                if len(parts) != 2:
                    continue

                station = parts[0]
                try:
                    temp = int(round(float(parts[1]) * 10))
                except ValueError:
                    continue

                if station not in self.results:
                    self.results[station] = [temp, temp, temp, 1]
                else:
                    stats = self.results[station]
                    if temp < stats[0]:
                        stats[0] = temp

                    if temp > stats[1]:
                        stats[1] = temp

                    stats[2] += temp
                    stats[3] += 1

        return self.results

    def format_results(self) -> str:
        """
        Formats the results int the expected ouput string
        """
        sorted_stations = sorted(self.results.keys())
        output = []

        for station in sorted_stations:
            min_temp, max_temp, total, count = self.results[station]
            mean_temp = (total / count) / 10.0
            min_temp /= 10.0
            max_temp /= 10.0
            output.append(f"{station}={min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}")
        return "{" + ", ".join(output) + "}"

    def validate(self, expected_output: Optional[str] = None) -> bool:
        """
        Runs the calculation and compares with expected output if provided.
        """

        print("Running baseline validation...")
        self.calculate()
        baseline_output = self.format_results()

        if expected_output:
            if baseline_output == expected_output:
                print("Validation PASSED!")
                return True
            else:
                print("Validation FAILED!")
                return False
        else:
            print("Baseline Result:")
            print(baseline_output)
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    validator = BaselineValidator(filename)
    validator.validate()


if __name__ == "__main__":
    main()
