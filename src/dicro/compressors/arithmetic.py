from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, str):
        return list(data)
    return list(data)


def arithmetic_encode(data: Any) -> Dict[str, Any]:
    seq = _as_list(data)
    if not seq:
        return {"algorithm": "arithmetic", "alphabet": [], "probabilities": {}, "tag": 0.0, "length": 0}

    counts = Counter(seq)
    alphabet = sorted(counts.keys(), key=lambda item: str(item))
    total = len(seq)
    probabilities = {symbol: counts[symbol] / total for symbol in alphabet}

    low = 0.0
    high = 1.0
    for symbol in seq:
        width = high - low
        cumulative = sum(probabilities[s] for s in alphabet if s < symbol)
        start = cumulative
        end = cumulative + probabilities[symbol]
        low, high = low + width * start, low + width * end

    tag = (low + high) / 2.0
    return {
        "algorithm": "arithmetic",
        "alphabet": alphabet,
        "probabilities": probabilities,
        "tag": tag,
        "length": len(seq),
    }


def arithmetic_decode(encoded: Dict[str, Any]) -> List[Any]:
    alphabet = encoded.get("alphabet", [])
    probabilities = encoded.get("probabilities", {})
    tag = encoded.get("tag", 0.0)
    length = encoded.get("length", 0)
    if not alphabet or length == 0:
        return []

    low = 0.0
    high = 1.0
    result: List[Any] = []
    for _ in range(length):
        width = high - low
        if width <= 0:
            return result
        value = (tag - low) / width

        cumulative = 0.0
        for symbol in alphabet:
            start = cumulative
            end = cumulative + probabilities[symbol]
            if start <= value < end:
                result.append(symbol)
                low, high = low + width * start, low + width * end
                break
            cumulative = end
    return result
