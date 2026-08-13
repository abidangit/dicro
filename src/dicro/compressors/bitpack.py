from __future__ import annotations

from typing import Any, Dict, List


def _as_int_list(data: Any) -> List[int]:
    if isinstance(data, (bytes, bytearray, memoryview)):
        return list(bytes(data))
    if isinstance(data, str):
        return [ord(ch) for ch in data]
    if isinstance(data, list):
        return [int(v) for v in data]
    return [int(data)]


def bitpack_encode(data: Any) -> Dict[str, Any]:
    values = _as_int_list(data)
    if not values:
        return {"algorithm": "bitpack", "width": 0, "payload": []}
    width = max(1, (max(values)).bit_length())
    bit_string = ""
    for value in values:
        bit_string += format(value, f"0{width}b")
    payload = [int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8)]
    if len(payload) == 0:
        payload = [0]
    return {"algorithm": "bitpack", "width": width, "payload": payload, "length": len(values)}


def bitpack_decode(encoded: Dict[str, Any]) -> List[int]:
    width = int(encoded.get("width", 8))
    payload = encoded.get("payload", [])
    if width <= 0 or not payload:
        return []
    bits = "".join(f"{byte:08b}" for byte in payload)
    values = []
    for offset in range(0, len(bits), width):
        chunk = bits[offset:offset + width]
        if len(chunk) < width:
            break
        values.append(int(chunk, 2))
    return values
