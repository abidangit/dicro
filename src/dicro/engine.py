from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .compressors.arithmetic import arithmetic_decode, arithmetic_encode
from .compressors.bitpack import bitpack_decode, bitpack_encode
from .compressors.burrows_wheeler import bwt_decode, bwt_encode
from .compressors.delta import delta_decode, delta_encode
from .compressors.huffman import huffman_decode, huffman_encode
from .compressors.lz77 import lz77_decode, lz77_encode
from .compressors.mtf import mtf_decode, mtf_encode
from .compressors.run_length import rle_decode, rle_encode
from .compressors.xor import xor_decode, xor_encode
from .core.normalizer import NormalizedData, normalize_data, restore_data
from .core.patterns import analyze_sequence


class CompressionEngine:
    """Pattern-aware universal compression engine for text, binary, JSON, and numeric data."""

    def __init__(self, algorithms: Optional[List[str]] = None):
        self.algorithms = algorithms or [
            "rle",
            "delta",
            "xor",
            "bitpack",
            "huffman",
            "arithmetic",
            "lz77",
            "bwt",
            "mtf",
        ]

    def analyze(self, data: Any) -> Dict[str, Any]:
        normalized = normalize_data(data)
        stats = analyze_sequence(normalized.payload)
        stats["input_kind"] = normalized.kind
        return stats

    def compress(self, data: Any, algorithms: Optional[List[str]] = None) -> Dict[str, Any]:
        normalized = normalize_data(data)
        candidates = []
        selected = algorithms or self.algorithms
        for name in selected:
            encoded = self._encode_by_name(name, normalized.payload)
            candidates.append({
                "algorithm": name,
                "encoded": encoded,
                "size": self._payload_size(encoded),
                "analysis": {**self.analyze(normalized.payload), "input_kind": normalized.kind},
                "input_kind": normalized.kind,
            })
        best = min(candidates, key=lambda item: (item["size"], item["algorithm"]))
        best["compression_ratio"] = round(len(normalized.payload) / max(1, best["size"]), 6)
        best["normalized_kind"] = normalized.kind
        return best

    def decompress(self, payload: Dict[str, Any]) -> Any:
        algorithm = payload["algorithm"]
        data = payload["encoded"]
        if algorithm == "rle":
            result = rle_decode(data)
        elif algorithm == "delta":
            result = delta_decode(data)
        elif algorithm == "xor":
            result = xor_decode(data)
        elif algorithm == "bitpack":
            result = bitpack_decode(data)
        elif algorithm == "huffman":
            result = huffman_decode(data)
        elif algorithm == "arithmetic":
            result = arithmetic_decode(data)
        elif algorithm == "lz77":
            result = lz77_decode(data)
        elif algorithm == "bwt":
            result = bwt_decode(data)
        elif algorithm == "mtf":
            result = mtf_decode(data)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        kind = payload.get("input_kind") or payload.get("analysis", {}).get("input_kind") or "list"
        return restore_data(NormalizedData(kind=kind, payload=result), algorithm=algorithm)

    def _encode_by_name(self, name: str, seq: List[Any]) -> Dict[str, Any]:
        if name == "rle":
            return rle_encode(seq)
        if name == "delta":
            return delta_encode(seq)
        if name == "xor":
            return xor_encode(seq)
        if name == "bitpack":
            return bitpack_encode(seq)
        if name == "huffman":
            return huffman_encode(seq)
        if name == "arithmetic":
            return arithmetic_encode(seq)
        if name == "lz77":
            return lz77_encode(seq)
        if name == "bwt":
            return bwt_encode(seq)
        if name == "mtf":
            return mtf_encode(seq)
        raise ValueError(f"Unsupported algorithm '{name}'")

    @staticmethod
    def _payload_size(payload: Dict[str, Any]) -> int:
        try:
            return len(json.dumps(payload, default=str, separators=(",", ":")))
        except Exception:
            return len(repr(payload))


__all__ = ["CompressionEngine"]
