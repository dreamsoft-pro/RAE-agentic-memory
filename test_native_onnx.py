import asyncio
import os
import sys
from pathlib import Path

# Add rae-core to path
sys.path.insert(0, str(Path(__file__).parent / "rae-core"))

from rae_core.embedding.native import NativeEmbeddingProvider

async def main():
    print("🚀 Testing NativeEmbeddingProvider (ONNX)...")
    
    # Path to downloaded model (cache)
    # We use explicit path from previous command output for robustness
    cache_dir = Path("/home/operator/.cache/huggingface/hub/models--nomic-ai--nomic-embed-text-v1.5/snapshots/e5cf08aadaa33385f5990def41f7a23405aec398")
    model_path = cache_dir / "onnx/model.onnx"
    tokenizer_path = cache_dir / "tokenizer.json"
    
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        return

    provider = NativeEmbeddingProvider(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        normalize=True
    )
    
    text = "search_query: What is the capital of France?"
    print(f"📝 Embedding: '{text}'")
    
    vector = await provider.embed_text(text)
    
    print(f"✅ Vector generated!")
    print(f"   Dimension: {len(vector)}")
    print(f"   Sample (first 5): {vector[:5]}")
    
    # Check normalization (L2 norm should be ~1.0)
    norm = sum(x*x for x in vector) ** 0.5
    print(f"   L2 Norm: {norm:.6f}")
    
    if 0.99 < norm < 1.01:
        print("✅ Normalization OK")
    else:
        print("❌ Normalization FAILED")

    # Test Matryoshka
    print("\n📦 Testing Matryoshka (256d)...")
    provider_small = NativeEmbeddingProvider(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        normalize=True,
        matryoshka_dim=256
    )
    vector_small = await provider_small.embed_text(text)
    print(f"✅ Small Vector generated!")
    print(f"   Dimension: {len(vector_small)}")
    print(f"   L2 Norm: {sum(x*x for x in vector_small) ** 0.5:.6f}")

if __name__ == "__main__":
    asyncio.run(main())
