from typing import Dict, List

from ..domain.models import TemperatureStats
from ..interfaces.protocols import ResultAggregator


class ParallellAggregator(ResultAggregator):
    """
    Aggregator results from multiple parallell processes
    """

    def aggregate(
        self, partial_results: List[Dict[str, List[int]]]
    ) -> Dict[str, TemperatureStats]:
        final_results = {}

        for partial_result in partial_results:
            for station, stats in partial_result.items():
                if station not in final_results:
                    final_results[station] = TemperatureStats(
                        stats[0], stats[1], stats[2], stats[3]
                    )
                else:
                    existing = final_results[station]

                    if stats[0] < existing.min_temp:
                        existing.min_temp = stats[0]

                    if stats[1] > existing.max_temp:
                        existing.max_temp = stats[1]

                    existing.sum_temp += stats[2]
                    existing.count += stats[3]

        return final_results
