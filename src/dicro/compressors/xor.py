from __future__ import annotations

from typing import Any, Dict, List


def _as_list(data: Any) -> List[int]:
    if isinstance(data, (bytes, bytearray, memoryview)):
        return list(bytes(data))
    if isinstance(data, str):
        return [ord(ch) for ch in data]
    if isinstance(data, list):
        return [int(v) for v in data]
    return [int(data)]


def xor_encode(data: Any, key: int = 0x5A) -> Dict[str, Any]:
    values = _as_list(data)
    encoded = [(value ^ key) & 0xFF for value in values]
    return {"algorithm": "xor", "key": key, "payload": encoded}


def xor_decode(encoded: Dict[str, Any]) -> List[int]:
    payload = encoded.get("payload", [])
    key = int(encoded.get("key", 0x5A))
    return [(value ^ key) & 0xFF for value in payload]
