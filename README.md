# Dicro

Dicro is a pattern-aware universal compression toolkit inspired by the Universal Pattern Engine concept: generate, transform, analyze, and discover sequence structure before selecting a compression strategy.

It is designed as a research-friendly, production-minded compression library with reusable sequence analysis and a complete compression stack for text, binary, numeric, and structured data.

## Motivation

The repository combines a few core ideas from the pattern-engine reference project:

- pattern-aware analysis of sequences
- transform-and-discover pipelines
- entropy and repetition metrics
- algorithm selection based on structure
- a single engine for encode/decode workflows

## Included algorithms and components

- Run-length encoding (RLE)
- Delta encoding
- XOR transform
- Bit-packing / numeric packing
- Huffman coding
- Arithmetic coding
- LZ77 dictionary compression
- Burrows-Wheeler transform (BWT)
- Move-to-front transform (MTF)
- pattern analysis and normalization for text, bytes, JSON, numbers, and lists
- single-engine selector for choosing the best strategy by payload profile

## Project structure

```text
src/
  dicro/
    __init__.py
    cli.py
    engine.py
    core/
      sequence.py
      patterns.py
    compressors/
      __init__.py
      run_length.py
      delta.py
      huffman.py
      arithmetic.py
      lz77.py
tests/
  test_dicro.py
```

## Quick start

```bash
python -m pip install -e .
dicro '"AAAAABBBBCCCCCDDD"'
```

Or from Python:

```python
from dicro import CompressionEngine

engine = CompressionEngine()
text = "AAAAABBBBCCCCCDDD"
result = engine.compress(text)
print(result["algorithm"])
print(engine.decompress(result))
```

## Standard validation

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Notes

This project is intentionally educational and extensible rather than a drop-in replacement for mature production compressors such as zstd, gzip, or LZMA. It is useful for experimentation, teaching, and building pattern-driven compression strategies.
