from __future__ import annotations

from typing import Any, Dict, List


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, str):
        return list(data)
    return list(data)


def lz77_encode(data: Any, window_size: int = 16) -> Dict[str, Any]:
    seq = _as_list(data)
    tokens: List[Dict[str, Any]] = []
    i = 0

    while i < len(seq):
        best_offset = 0
        best_length = 0
        max_offset = min(window_size, i)

        for offset in range(1, max_offset + 1):
            length = 0
            while i + length < len(seq) and length < window_size:
                if seq[i - offset + length] != seq[i + length]:
                    break
                length += 1
            if length > best_length:
                best_length = length
                best_offset = offset

        if best_length > 1:
            tokens.append({"op": "copy", "offset": best_offset, "length": best_length})
            i += best_length
        else:
            tokens.append({"op": "literal", "value": seq[i]})
            i += 1

    return {"algorithm": "lz77", "window_size": window_size, "tokens": tokens}


def lz77_decode(encoded: Dict[str, Any]) -> List[Any]:
    tokens = encoded.get("tokens", [])
    output: List[Any] = []

    for token in tokens:
        if token["op"] == "literal":
            output.append(token["value"])
        else:
            offset = token["offset"]
            length = token["length"]
            start = len(output) - offset
            for _ in range(length):
                output.append(output[start])
                start += 1
    return output
