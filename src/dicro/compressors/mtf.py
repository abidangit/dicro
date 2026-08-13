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


def mtf_encode(data: Any) -> Dict[str, Any]:
    values = _as_list(data)
    alphabet = []
    output: List[int] = []
    for symbol in values:
        if symbol not in alphabet:
            alphabet.append(symbol)
        index = alphabet.index(symbol)
        output.append(index)
        alphabet.pop(index)
        alphabet.insert(0, symbol)
    return {"algorithm": "mtf", "data": output, "alphabet": list(dict.fromkeys(values))}


def mtf_decode(encoded: Dict[str, Any]) -> List[Any]:
    data = encoded.get("data", [])
    alphabet = encoded.get("alphabet", [])
    if not alphabet:
        alphabet = []
    output: List[Any] = []
    for index in data:
        symbol = alphabet[index]
        output.append(symbol)
        alphabet.pop(index)
        alphabet.insert(0, symbol)
    return output
