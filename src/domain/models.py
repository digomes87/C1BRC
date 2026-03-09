from dataclasses import dataclass
from typing import Dict


@dataclass
class TemperatureStats:
    """
    Represents the statistics for a single station
    Using dataclass for clear structure, tough raw list are faster for tight loops
    """

    min_temp: int
    max_temp: int
    sum_temp: int
    count: int

    def merge(self, other: "TemperatureStats") -> None:
        if other.min_temp < self.min_temp:
            self.min_temp = other.min_temp

        if other.max_temp > self.max_temp:
            self.max_temp = other.max_temp

        self.sum_temp += other.sum_temp
        self.count += other.count

    @property
    def mean(self) -> float:
        if self.count == 0:
            return 0.0

        return (self.sum_temp / self.count) / 10.0

    @property
    def min_float(self) -> float:
        return self.min_temp / 10.0

    @property
    def max_float(self) -> float:
        return self.max_temp / 10.0


class StationRegistry:
    """
    Registry to mannage station station
    """

    def __init__(self):
        self._stats: Dict[str, TemperatureStats] = {}

    def add_reading(self, station: str, temp: int) -> None:
        if station not in self._stats:
            self._stats[station] = TemperatureStats(temp, temp, temp, 1)
        else:
            stat = self._stats[station]
            if temp < stat.min_temp:
                stat.min_temp = temp

            if temp > stat.max_temp:
                stat.max_temp = temp

            stat.sum_temp += temp
            stat.count += 1

    def merge_registry(self, other: "StationRegistry") -> None:
        for station, stats in other._stats.items():
            if station not in self._stats:
                self._stats[station] = stats
            else:
                self._stats[station].merge(stats)

    def get_all_stats(self) -> Dict[str, TemperatureStats]:
        return self._stats
