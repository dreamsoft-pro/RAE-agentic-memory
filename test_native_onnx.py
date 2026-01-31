import asyncio
import sys
from pathlib import Path

# Add rae-core to path
sys.path.insert(0, str(Path(__file__).parent / "rae-core"))

from rae_core.embedding.native import NativeEmbeddingProvider


async def main():
    print("🚀 Testing NativeEmbeddingProvider (ONNX)...")

    # Path to downloaded model (cache)
    model_path = Path("models/all-MiniLM-L6-v2/model.onnx")
    tokenizer_path = Path("models/all-MiniLM-L6-v2/tokenizer.json")

    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        return

    provider = NativeEmbeddingProvider(
        model_path=model_path, tokenizer_path=tokenizer_path, normalize=True
    )

    text = "search_query: What is the capital of France?"
    print(f"📝 Embedding: '{text}'")

    vector = await provider.embed_text(text)

    print("✅ Vector generated!")
    print(f"   Dimension: {len(vector)}")
    print(f"   Sample (first 5): {vector[:5]}")

    # Check normalization (L2 norm should be ~1.0)
    norm = sum(x * x for x in vector) ** 0.5
    print(f"   L2 Norm: {norm:.6f}")

    if 0.99 < norm < 1.01:
        print("✅ Normalization OK")
    else:
        print("❌ Normalization FAILED")


if __name__ == "__main__":
    asyncio.run(main())
