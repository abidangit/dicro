from dicro import CompressionEngine
from dicro.compressors.arithmetic import arithmetic_decode, arithmetic_encode
from dicro.compressors.bitpack import bitpack_decode, bitpack_encode
from dicro.compressors.burrows_wheeler import bwt_decode, bwt_encode
from dicro.compressors.delta import delta_decode, delta_encode
from dicro.compressors.huffman import huffman_decode, huffman_encode
from dicro.compressors.lz77 import lz77_decode, lz77_encode
from dicro.compressors.mtf import mtf_decode, mtf_encode
from dicro.compressors.run_length import rle_decode, rle_encode
from dicro.compressors.xor import xor_decode, xor_encode


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


def test_xor_round_trip():
    data = [10, 20, 30, 40, 50]
    encoded = xor_encode(data)
    assert xor_decode(encoded) == data


def test_bitpack_round_trip():
    data = [1, 2, 3, 4, 5]
    encoded = bitpack_encode(data)
    assert bitpack_decode(encoded) == data


def test_bwt_round_trip():
    data = ["b", "a", "n", "a", "n", "a"]
    encoded = bwt_encode(data)
    assert bwt_decode(encoded) == data


def test_mtf_round_trip():
    data = ["b", "a", "n", "a", "n", "a"]
    encoded = mtf_encode(data)
    assert mtf_decode(encoded) == data


def test_engine_selects_best_algorithm_and_round_trips_string():
    engine = CompressionEngine()
    data = "AAAAABBBBCCCCCDDD"
    result = engine.compress(data)
    assert result["algorithm"] in {"rle", "delta", "xor", "bitpack", "huffman", "arithmetic", "lz77", "bwt", "mtf"}
    assert engine.decompress(result) == data
