import asyncio
import time
import numpy as np
import os
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "rae-core"))

from rae_core.embedding.native import NativeEmbeddingProvider

async def test_speed():
    model_path = os.getenv("ONNX_EMBEDDER_PATH", "models/nomic-embed-text-v1.5/model.onnx")
    tokenizer_path = model_path.replace("model.onnx", "tokenizer.json")
    
    print(f"🧐 Initializing Provider with: {model_path}")
    try:
        provider = NativeEmbeddingProvider(
            model_path=model_path,
            tokenizer_path=tokenizer_path
        )
    except Exception as e:
        print(f"❌ Failed to init: {e}")
        return

    print(f"✅ Providers available: {provider.session.get_providers()}")
    print(f"✅ Active Provider: {provider.session.get_provider_options().keys()}")

    texts = ["This is a test sentence for benchmarking GPU speed."] * 100
    
    print(f"🚀 Benchmarking 100 embeddings (Batch size 100)...")
    start = time.time()
    await provider.embed_batch(texts)
    end = time.time()
    
    print(f"⏱️ Total time for 100: {end - start:.4f}s")
    print(f"⏱️ Average per text: {(end - start)/100:.4f}s")

if __name__ == "__main__":
    asyncio.run(test_speed())
