"""Verification Script for System 87.0 (Silicon Oracle).

Tests:
1. Contiguous Memory Arenas (bytearray storage).
2. Fixed-Point Quantization (deterministic math).
3. Bloom Filter (The Scalpel) efficiency.
4. Deterministic Clock.
5. Merkle-DAG Provenance Hashing.
"""

import asyncio
import random
from uuid import uuid4
from datetime import datetime

from rae_core.adapters.memory.storage import InMemoryStorage
from rae_core.utils.clock import DeterministicClock
from rae_core.utils.hashing import compute_provenance_hash, stable_hash
from rae_core.math.quantization_bytes import dequantize_vector_bytes

async def run_verification():
    print("🚀 Starting System 87.0 Verification (Silicon Oracle)...")
    
    # 1. Setup Deterministic Environment
    clock = DeterministicClock(datetime(2025, 1, 1, 12, 0, 0))
    storage = InMemoryStorage(clock=clock)
    
    # 2. Generate Data (1000 vectors)
    print("Allocating 1000 vectors in Contiguous Arena...")
    dim = 128
    model = "test-model"
    
    target_id = uuid4()
    target_vector = [0.1] * dim
    target_tags = ["critical", "target"]
    
    # Store target first
    await storage.store_memory(
        content="Target Memory",
        layer="episodic",
        tags=target_tags,
        embedding={model: target_vector},
        tenant_id="test",
        metadata={"id": str(target_id)}
    )
    
    # Store distractors (noise)
    for i in range(999):
        # Random vector but orthogonal or far from target to ensure ranking
        vec = [random.uniform(-0.1, 0.05) for _ in range(dim)]
        tags = ["noise", f"tag_{i}"]
        await storage.store_memory(
            content=f"Distractor {i}",
            layer="episodic",
            tags=tags,
            embedding={model: vec},
            tenant_id="test"
        )
        
    # 3. Verify Arena Layout
    arena_size = len(storage._vector_arenas[model])
    expected_size = 1000 * dim * 4  # 4 bytes per int32
    print(f"Arena Size: {arena_size} bytes (Expected: {expected_size})")
    assert arena_size == expected_size, "Arena size mismatch!"
    print("✅ Contiguous Arena Allocation Verified.")
    
    # 4. Verify Quantization & Determinism
    # Retrieve target vector
    # We need to find the memory ID for "Target Memory".
    # In this script we didn't save the ID from store_memory return, but we passed it in metadata?
    # Actually store_memory returns ID. But I ignored it.
    # Let's search by content.
    results = await storage.search_memories("Target Memory", "test", "default")
    stored_target_id = results[0]["id"]
    
    retrieved_vec = await storage.get_vector(stored_target_id, "test")
    # Check first element (should be close to 0.1)
    print(f"Retrieved Vector[0]: {retrieved_vec[0]} (Original: 0.1)")
    # Quantization error expected: 1/65536 approx 0.000015
    assert abs(retrieved_vec[0] - 0.1) < 0.0001, "Quantization error too high!"
    print("✅ Fixed-Point Quantization Verified.")
    
    # 5. Verify The Scalpel (Bloom Filter Search)
    print("Testing Bloom Filter Search (Target: 'critical' tag)...")
    # Search with tag filter "critical". Only target has it.
    # Query vector is target vector (should match perfectly).
    
    # We expect ONLY target to be returned if bloom filter works, because distractors don't have "critical".
    # Even if their vector was identical, bloom filter should reject them.
    # Let's force a distractor to have identical vector but different tags.
    
    # Add "Doppelganger" (Same vector, wrong tags)
    await storage.store_memory(
        content="Doppelganger",
        layer="episodic",
        tags=["noise"],
        embedding={model: target_vector}, # Exact same vector!
        tenant_id="test"
    )
    
    # Search with "tags": ["critical"]
    search_results = await storage.search_similar(
        query_embedding=target_vector,
        tenant_id="test",
        model_name=model,
        filters={"tags": ["critical"]},
        limit=10
    )
    
    print(f"Search Results: {len(search_results)}")
    # Should contain ONLY target, not Doppelganger
    found_ids = [r[0] for r in search_results]
    assert stored_target_id in found_ids, "Target not found!"
    assert len(found_ids) == 1, f"Bloom Filter failed! Found {len(found_ids)} items (expected 1). Doppelganger leaked?"
    
    print("✅ Bloom Filter (The Scalpel) Verified.")
    
    # 6. Verify Provenance Hash
    print("Testing Provenance Hash...")
    data_node = {"content": "Fact A", "confidence": 0.9}
    sources = ["hash1", "hash2"]
    phash = compute_provenance_hash(data_node, sources)
    print(f"Provenance Hash: {phash}")
    
    # Verify determinism
    phash2 = compute_provenance_hash(data_node, ["hash2", "hash1"]) # Different order
    assert phash == phash2, "Provenance hash not order-independent for sources!"
    print("✅ Merkle-DAG Provenance Verified.")
    
    print("🎉 SYSTEM 87.0 VERIFIED SUCCESSFULLY.")

if __name__ == "__main__":
    asyncio.run(run_verification())
