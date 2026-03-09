from typing import Dict

from ..domain.models import TemperatureStats
from ..interfaces.protocols import ResultFormatter


class DefaultFormatter(ResultFormatter):
    """
    formats results as required by the brc challege
    """

    def format(self, results: Dict[str, TemperatureStats]) -> str:
        sorted_stations = sorted(results.keys())
        output = []

        for station in sorted_stations:
            stats = results[station]
            output.append(
                f"{station}={stats.min_float:.1f}/{stats.mean:.1f}/{stats.max_float:.1f}"
            )

        return "{" + ", ".join(output) + "}"
