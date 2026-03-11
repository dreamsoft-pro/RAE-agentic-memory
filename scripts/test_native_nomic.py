
import os
import sys
import numpy as np
import time

def test_nomic():
    try:
        import onnxruntime as ort
        from tokenizers import Tokenizer
        print("✅ Libraries imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import libraries: {e}")
        return

    model_path = "models/nomic-embed-text-v1.5/model.onnx"
    tokenizer_path = "models/nomic-embed-text-v1.5/tokenizer.json"

    if not os.path.exists(model_path):
        print(f"❌ Model file missing: {model_path}")
        return

    print(f"📂 Model size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")

    try:
        print("🔄 Loading tokenizer...")
        tokenizer = Tokenizer.from_file(tokenizer_path)
        
        print("🔄 Loading ONNX session (CPU)...")
        # Force CPU to avoid driver issues during test
        session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        
        print("🔍 Testing inference...")
        text = "search_document: RAE Agnostic Hive Mind test"
        encoded = tokenizer.encode(text)
        
        # Prepare inputs including token_type_ids
        inputs = {
            "input_ids": np.array([encoded.ids], dtype=np.int64),
            "attention_mask": np.array([encoded.attention_mask], dtype=np.int64),
            "token_type_ids": np.array([encoded.type_ids], dtype=np.int64)
        }
        
        start = time.time()
        outputs = session.run(None, inputs)
        duration = time.time() - start
        
        print(f"✨ SUCCESS!")
        print(f"📏 Vector dimension: {outputs[0].shape[-1]}")
        print(f"⏱️  Inference time: {duration:.4f}s")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    test_nomic()
