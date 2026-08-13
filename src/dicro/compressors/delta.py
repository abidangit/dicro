from __future__ import annotations

from typing import Any, Dict, List


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, str):
        return list(data)
    return list(data)


def delta_encode(data: Any) -> Dict[str, Any]:
    seq = _as_list(data)
    if not seq:
        return {"algorithm": "delta", "values": []}

    deltas = [seq[0]]
    for prev, curr in zip(seq, seq[1:]):
        deltas.append(curr - prev)
    return {"algorithm": "delta", "values": deltas}


def delta_decode(encoded: Dict[str, Any]) -> List[Any]:
    values = encoded.get("values", [])
    if not values:
        return []

    result = [values[0]]
    for delta in values[1:]:
        result.append(result[-1] + delta)
    return result
