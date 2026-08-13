from dicro import CompressionEngine
from dicro.compressors.arithmetic import arithmetic_decode, arithmetic_encode
from dicro.compressors.delta import delta_decode, delta_encode
from dicro.compressors.huffman import huffman_decode, huffman_encode
from dicro.compressors.lz77 import lz77_decode, lz77_encode
from dicro.compressors.run_length import rle_decode, rle_encode


def test_rle_round_trip():
    data = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    encoded = rle_encode(data)
    assert rle_decode(encoded) == data


def test_delta_round_trip():
    data = [3, 5, 8, 12, 17]
    encoded = delta_encode(data)
    assert delta_decode(encoded) == data


def test_huffman_round_trip():
    data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    encoded = huffman_encode(data)
    assert huffman_decode(encoded) == data


def test_arithmetic_round_trip():
    data = [1, 1, 1, 2, 2, 2, 2, 3, 3]
    encoded = arithmetic_encode(data)
    assert arithmetic_decode(encoded) == data


def test_lz77_round_trip():
    data = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4]
    encoded = lz77_encode(data)
    assert lz77_decode(encoded) == data


def test_engine_selects_best_algorithm_and_round_trips_string():
    engine = CompressionEngine()
    data = "AAAAABBBBCCCCCDDD"
    result = engine.compress(data)
    assert result["algorithm"] in {"rle", "delta", "huffman", "arithmetic", "lz77"}
    assert engine.decompress(result) == data
