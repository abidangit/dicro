from __future__ import annotations

import argparse
import json
from typing import Any

from .engine import CompressionEngine


def _parse_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def main() -> None:
    parser = argparse.ArgumentParser(description="Pattern-aware universal compression engine")
    parser.add_argument("value", help="Data to compress, as JSON or raw text")
    parser.add_argument("--algorithm", choices=["rle", "delta", "huffman", "arithmetic", "lz77"], help="Specific algorithm to use")
    args = parser.parse_args()

    engine = CompressionEngine()
    data = _parse_value(args.value)
    if args.algorithm:
        result = engine.compress(data, algorithms=[args.algorithm])
    else:
        result = engine.compress(data)
    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
