import pytest
import datetime
from rae_core.utils.hashing import stable_hash, bloom_filter_fingerprint, compute_provenance_hash

def test_stable_hash_string():
    h1 = stable_hash("test-string")
    h2 = stable_hash("test-string")
    assert isinstance(h1, int)
    assert h1 == h2
    # Check if it fits in 64-bit signed int
    assert -2**63 <= h1 < 2**63

def test_stable_hash_bytes():
    data = b"\x00\x01\x02\x03"
    h1 = stable_hash(data)
    h2 = stable_hash(data)
    assert h1 == h2
    assert isinstance(h1, int)

def test_stable_hash_different_inputs():
    assert stable_hash("a") != stable_hash("b")
    assert stable_hash("a") == stable_hash(b"a")

def test_bloom_filter_fingerprint_empty():
    assert bloom_filter_fingerprint([]) == 0

def test_bloom_filter_fingerprint_single():
    mask = bloom_filter_fingerprint(["tag1"])
    assert mask > 0
    assert (mask & (mask - 1)) == 0  # Should be a power of 2 since it's a single bit

def test_bloom_filter_fingerprint_multiple():
    mask1 = bloom_filter_fingerprint(["tag1"])
    mask2 = bloom_filter_fingerprint(["tag2"])
    mask_both = bloom_filter_fingerprint(["tag1", "tag2"])
    assert mask_both == mask1 | mask2

def test_compute_provenance_hash_happy_path():
    data = {"content": "hello", "type": "message"}
    sources = ["hash1", "hash2"]
    h = compute_provenance_hash(data, sources)
    assert isinstance(h, str)
    assert len(h) == 64  # SHA-256 hex length

def test_compute_provenance_hash_determinism():
    data = {"content": "hello", "type": "message"}
    sources = ["hash1", "hash2"]
    assert compute_provenance_hash(data, sources) == compute_provenance_hash(data, sources)

def test_compute_provenance_hash_key_order_independence():
    data1 = {"a": 1, "b": 2}
    data2 = {"b": 2, "a": 1}
    sources = ["h1", "h2"]
    assert compute_provenance_hash(data1, sources) == compute_provenance_hash(data2, sources)

def test_compute_provenance_hash_source_order_independence():
    data = {"content": "test"}
    sources1 = ["h1", "h2"]
    sources2 = ["h2", "h1"]
    assert compute_provenance_hash(data, sources1) == compute_provenance_hash(data, sources2)

def test_compute_provenance_hash_ignores_volatile_fields():
    data1 = {"content": "test", "access_count": 10}
    data2 = {"content": "test", "access_count": 20, "usage_count": 5, "last_accessed_at": "now"}
    sources = ["h1"]
    assert compute_provenance_hash(data1, sources) == compute_provenance_hash(data2, sources)

def test_compute_provenance_hash_non_serializable_fallback():
    # compute_provenance_hash uses json.dumps(..., default=str)
    data1 = {"time": datetime.datetime(2023, 1, 1)}
    data2 = {"time": "2023-01-01 00:00:00"}
    sources = []
    # datetime defaults to str() which might be slightly different depending on format
    # but it shouldn't crash.
    h = compute_provenance_hash(data1, sources)
    assert isinstance(h, str)

def test_compute_provenance_hash_empty_inputs():
    assert compute_provenance_hash({}, []) is not None
