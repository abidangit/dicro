from __future__ import annotations

from typing import Any, Dict, List


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray, memoryview)):
        return list(bytes(data))
    if isinstance(data, str):
        return list(data)
    if isinstance(data, list):
        return list(data)
    return [data]


def bwt_encode(data: Any) -> Dict[str, Any]:
    values = _as_list(data)
    if not values:
        return {"algorithm": "bwt", "data": [], "primary_index": 0, "rows": []}
    rotations = [tuple(values[i:] + values[:i]) for i in range(len(values))]
    sorted_rotations = sorted(rotations)
    primary_index = sorted_rotations.index(tuple(values))
    transformed = [row[-1] for row in sorted_rotations]
    return {
        "algorithm": "bwt",
        "data": transformed,
        "primary_index": primary_index,
        "rows": [list(row) for row in sorted_rotations],
    }


def bwt_decode(encoded: Dict[str, Any]) -> List[Any]:
    rows = encoded.get("rows", [])
    if rows:
        primary_index = int(encoded.get("primary_index", 0))
        return list(rows[primary_index])
    transformed = encoded.get("data", [])
    if not transformed:
        return []
    return transformed
