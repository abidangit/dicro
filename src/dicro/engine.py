from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .compressors.arithmetic import arithmetic_decode, arithmetic_encode
from .compressors.delta import delta_decode, delta_encode
from .compressors.huffman import huffman_decode, huffman_encode
from .compressors.lz77 import lz77_decode, lz77_encode
from .compressors.run_length import rle_decode, rle_encode
from .core.patterns import analyze_sequence


class CompressionEngine:
    """Pattern-aware compression engine that chooses the best strategy for a dataset."""

    def __init__(self, algorithms: Optional[List[str]] = None):
        self.algorithms = algorithms or ["rle", "delta", "huffman", "arithmetic", "lz77"]

    def analyze(self, data: Any) -> Dict[str, Any]:
        seq, input_kind = self._normalize_for_analysis(data)
        stats = analyze_sequence(seq)
        stats["input_kind"] = input_kind
        return stats

    def compress(self, data: Any, algorithms: Optional[List[str]] = None) -> Dict[str, Any]:
        seq, input_kind = self._normalize_for_analysis(data)
        candidates = []
        selected = algorithms or self.algorithms
        for name in selected:
            encoded = self._encode_by_name(name, seq)
            candidates.append({
                "algorithm": name,
                "encoded": encoded,
                "size": self._payload_size(encoded),
                "analysis": {**self.analyze(seq), "input_kind": input_kind},
                "input_kind": input_kind,
            })
        best = min(candidates, key=lambda item: (item["size"], item["algorithm"]))
        best["compression_ratio"] = round(len(seq) / max(1, best["size"]), 6)
        return best

    def decompress(self, payload: Dict[str, Any]) -> Any:
        algorithm = payload["algorithm"]
        data = payload["encoded"]
        if algorithm == "rle":
            result = rle_decode(data)
        elif algorithm == "delta":
            result = delta_decode(data)
        elif algorithm == "huffman":
            result = huffman_decode(data)
        elif algorithm == "arithmetic":
            result = arithmetic_decode(data)
        elif algorithm == "lz77":
            result = lz77_decode(data)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        kind = payload.get("input_kind") or payload.get("analysis", {}).get("input_kind")
        if kind == "str":
            return "".join(str(item) for item in result)
        if kind == "bytes":
            return bytes(result)
        if kind == "json":
            return json.loads("".join(str(item) for item in result))
        return result

    def _normalize_for_analysis(self, data: Any):
        if isinstance(data, (bytes, bytearray)):
            return list(data), "bytes"
        if isinstance(data, str):
            return list(data), "str"
        if isinstance(data, dict):
            payload = json.dumps(data, separators=(",", ":"), sort_keys=True)
            return list(payload), "json"
        if isinstance(data, (list, tuple, set)):
            return list(data), "list"
        return [data], "scalar"

    def _encode_by_name(self, name: str, seq: List[Any]) -> Dict[str, Any]:
        if name == "rle":
            return rle_encode(seq)
        if name == "delta":
            return delta_encode(seq)
        if name == "huffman":
            return huffman_encode(seq)
        if name == "arithmetic":
            return arithmetic_encode(seq)
        if name == "lz77":
            return lz77_encode(seq)
        raise ValueError(f"Unsupported algorithm '{name}'")

    @staticmethod
    def _payload_size(payload: Dict[str, Any]) -> int:
        try:
            return len(json.dumps(payload, default=str, separators=(",", ":")))
        except Exception:
            return len(repr(payload))


__all__ = ["CompressionEngine"]
