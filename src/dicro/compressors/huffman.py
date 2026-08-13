from __future__ import annotations

import heapq
from collections import Counter
from typing import Any, Dict, List


class _Node:
    def __init__(self, symbol=None, weight=0, left=None, right=None):
        self.symbol = symbol
        self.weight = weight
        self.left = left
        self.right = right


def _as_list(data: Any) -> List[Any]:
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, str):
        return list(data)
    return list(data)


def _build_codebook(symbols: List[Any]) -> Dict[Any, str]:
    counts = Counter(symbols)
    if not counts:
        return {}
    if len(counts) == 1:
        symbol, _ = next(iter(counts.items()))
        return {symbol: "0"}

    heap = []
    for symbol, weight in counts.items():
        node = _Node(symbol=symbol, weight=weight)
        heapq.heappush(heap, (weight, len(heap), node))

    while len(heap) > 1:
        _, _, left = heapq.heappop(heap)
        _, _, right = heapq.heappop(heap)
        merged = _Node(weight=left.weight + right.weight, left=left, right=right)
        heapq.heappush(heap, (merged.weight, len(heap), merged))

    root = heap[0][2]
    codes: Dict[Any, str] = {}

    def walk(node: _Node, prefix: str):
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(root, "")
    return codes


def huffman_encode(data: Any) -> Dict[str, Any]:
    seq = _as_list(data)
    if not seq:
        return {"algorithm": "huffman", "codebook": [], "payload": []}

    codebook = _build_codebook(seq)
    payload = []
    for symbol in seq:
        payload.extend(int(bit) for bit in codebook[symbol])

    serialized = [[symbol, codebook[symbol]] for symbol in sorted(codebook, key=lambda x: str(x))]
    return {"algorithm": "huffman", "codebook": serialized, "payload": payload}


def huffman_decode(encoded: Dict[str, Any]) -> List[Any]:
    codebook = encoded.get("codebook", [])
    payload = encoded.get("payload", [])
    if not codebook or not payload:
        return []

    reverse = {code: symbol for symbol, code in codebook}
    output: List[Any] = []
    current = ""
    for bit in payload:
        current += str(bit)
        if current in reverse:
            output.append(reverse[current])
            current = ""
    return output
