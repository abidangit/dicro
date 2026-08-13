from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, List, Optional


class Sequence:
    """Sequence wrapper used for pattern analysis and compression heuristics."""

    def __init__(self, values: Iterable[float]):
        self.values = list(values)

    @classmethod
    def from_list(cls, values: Iterable[float]) -> "Sequence":
        return cls(values)

    @property
    def length(self) -> int:
        return len(self.values)

    def differences(self, order: int = 1) -> List[List[float]]:
        result: List[List[float]] = []
        current = list(self.values)
        for _ in range(order):
            if len(current) < 2:
                break
            current = [current[i + 1] - current[i] for i in range(len(current) - 1)]
            result.append(current)
        return result

    def is_constant_difference(self, order: int = 1) -> bool:
        diffs = self.differences(order)
        if not diffs:
            return False
        last = diffs[-1]
        return bool(last) and all(abs(x - last[0]) < 1e-9 for x in last)

    def entropy(self) -> float:
        if not self.values:
            return 0.0
        counts = Counter(self.values)
        total = len(self.values)
        entropy = 0.0
        for count in counts.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        return entropy

    def dominant_symbol(self):
        if not self.values:
            return None
        counts = Counter(self.values)
        return counts.most_common(1)[0][0]

    def repetition_score(self) -> float:
        if not self.values:
            return 0.0
        counts = Counter(self.values)
        return max(counts.values()) / len(self.values)
