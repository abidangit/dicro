from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class NormalizedData:
    kind: str
    payload: List[Any]
    original: Any | None = None


def normalize_data(data: Any) -> NormalizedData:
    if data is None:
        return NormalizedData("scalar", [None], data)
    if isinstance(data, (bytes, bytearray, memoryview)):
        return NormalizedData("bytes", list(bytes(data)), data)
    if isinstance(data, str):
        return NormalizedData("text", list(data), data)
    if isinstance(data, dict):
        return NormalizedData("json", list(json.dumps(data, sort_keys=True, separators=(",", ":"))), data)
    if isinstance(data, (list, tuple, set)):
        return NormalizedData("list", list(data), data)
    if isinstance(data, (int, float, bool)):
        return NormalizedData("scalar", [data], data)
    try:
        return NormalizedData("iterable", list(data), data)
    except TypeError:
        return NormalizedData("scalar", [str(data)], data)


def restore_data(normalized: NormalizedData, algorithm: str | None = None) -> Any:
    kind = normalized.kind
    payload = normalized.payload
    if kind == "bytes":
        return bytes(payload)
    if kind == "text":
        if payload and all(isinstance(item, int) for item in payload):
            return "".join(chr(item) for item in payload)
        return "".join(str(item) for item in payload)
    if kind == "json":
        text = "".join(str(item) for item in payload)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    if kind == "list":
        return payload
    if kind == "scalar":
        return payload[0] if payload else None
    if kind == "iterable":
        return payload
    return payload
