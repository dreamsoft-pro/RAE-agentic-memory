"""
Script to download a small ONNX LLM for RAE-Lite.
Used before building the EXE to ensure the model is bundled.
"""

import os
import shutil
from pathlib import Path

def download_llm():
    # Target directory
    model_dir = Path("models/llm")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Preparing to download local LLM to {model_dir}")
    print("Zalecany model: Phi-3-mini-4k-instruct-onnx")
    
    # In a real scenario, we would use huggingface_hub to download
    try:
        from huggingface_hub import snapshot_download
        print("📥 Downloading from Hugging Face...")
        snapshot_download(
            repo_id="microsoft/Phi-3-mini-4k-instruct-onnx",
            revision="main",
            allow_patterns=["cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/*"],
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        
        # Move files from subfolder if necessary
        src_path = model_dir / "cpu_and_mobile" / "cpu-int4-rtn-block-32-acc-level-4"
        if src_path.exists():
            for f in src_path.iterdir():
                shutil.move(str(f), str(model_dir))
            shutil.rmtree(str(model_dir / "cpu_and_mobile"))
            
        print("✅ Local LLM downloaded successfully.")
    except ImportError:
        print("❌ Error: 'huggingface_hub' not installed. Run 'pip install huggingface_hub'.")
    except Exception as e:
        print(f"❌ Download failed: {e}")

if __name__ == "__main__":
    download_llm()
