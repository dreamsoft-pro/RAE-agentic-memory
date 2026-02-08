import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "rae-core"))

from rae_core.embedding.native import NativeEmbeddingProvider


async def verify():
    print("🔍 Verifying GPU Support...")

    # Mock config flow
    use_gpu = os.getenv("RAE_USE_GPU", "false").lower() == "true"
    print(f"⚙️  RAE_USE_GPU={use_gpu}")

    model_path = "models/nomic-embed-text-v1.5/model.onnx"
    # Ensure model exists or use dummy
    if not os.path.exists(model_path):
        print(f"⚠️  Model not found at {model_path}, checking alternative...")
        # fallback for testing
        model_path = "models/all-MiniLM-L6-v2/model.onnx"

    if not os.path.exists(model_path):
         print("❌ No ONNX model found. Cannot verify.")
         return

    tokenizer_path = model_path.replace("model.onnx", "tokenizer.json")

    try:
        provider = NativeEmbeddingProvider(
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            use_gpu=use_gpu
        )
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return

    providers = provider.session.get_providers()
    print(f"✅ Available Providers: {providers}")

    provider.session.get_provider_options().keys()
    # Note: get_provider_options returns dict of options for active providers

    if use_gpu:
        if "CUDAExecutionProvider" in providers:
            print("🎉 CUDA IS ACTIVE!")
        else:
            print("⚠️  CUDA requested but NOT active. (Missing libs?)")
    else:
        print("ℹ️  CPU Mode (Expected).")

if __name__ == "__main__":
    asyncio.run(verify())
