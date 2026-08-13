from __future__ import annotations

from typing import Any, Dict, Iterable, List


def classify_sequence(seq: Iterable[Any]) -> str:
    values = list(seq)
    if not values:
        return "empty"
    if len(set(values)) == 1:
        return "constant"

    if len(values) >= 3:
        diffs = [b - a for a, b in zip(values, values[1:])]
        if diffs and all(d == diffs[0] for d in diffs):
            return "arithmetic"

    if len(values) >= 3:
        ratios = []
        valid = True
        for a, b in zip(values, values[1:]):
            if a == 0:
                valid = False
                break
            ratios.append(b / a)
        if valid and ratios and all(abs(r - ratios[0]) < 1e-9 for r in ratios):
            return "geometric"

    if len(values) >= 3 and any(values[i] == values[i + 1] for i in range(len(values) - 1)):
        return "repetitive"

    return "mixed"


def analyze_sequence(seq: Iterable[Any]) -> Dict[str, Any]:
    values = list(seq)
    if not values:
        return {"length": 0, "unique_symbols": 0, "classification": "empty", "entropy": 0.0, "repetition": 0.0, "dominant_symbol": None}

    unique = set(values)
    counts = {}
    for item in values:
        counts[item] = counts.get(item, 0) + 1

    dominant = max(counts.items(), key=lambda item: item[1])[0]
    entropy = 0.0
    total = len(values)
    for count in counts.values():
        p = count / total
        entropy -= p * __import__("math").log2(p)

    repetition = max(counts.values()) / total
    return {
        "length": len(values),
        "unique_symbols": len(unique),
        "classification": classify_sequence(values),
        "entropy": round(entropy, 6),
        "repetition": round(repetition, 6),
        "dominant_symbol": dominant,
    }
