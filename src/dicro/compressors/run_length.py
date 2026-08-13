from __future__ import annotations

from typing import Any, Dict, List


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, str):
        return list(data)
    return list(data)


def rle_encode(data: Any) -> Dict[str, Any]:
    seq = _as_list(data)
    if not seq:
        return {"algorithm": "rle", "runs": []}

    runs: List[Dict[str, Any]] = []
    current = seq[0]
    count = 1
    for item in seq[1:]:
        if item == current:
            count += 1
        else:
            runs.append({"value": current, "count": count})
            current = item
            count = 1
    runs.append({"value": current, "count": count})
    return {"algorithm": "rle", "runs": runs}


def rle_decode(encoded: Dict[str, Any]) -> List[Any]:
    runs = encoded.get("runs", [])
    result: List[Any] = []
    for run in runs:
        result.extend([run["value"]] * run["count"])
    return result
