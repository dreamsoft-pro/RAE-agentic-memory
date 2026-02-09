import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, dest_path: Path):
    """Download a file with progress bar."""
    if dest_path.exists():
        # Check size if it matches expectation roughly?
        # For now, if user says "re-download", maybe we should overwrite if size is wrong.
        # But let's assume if exists, it's fine unless forced.
        # User complained about 500MB vs 130MB.
        size = dest_path.stat().st_size
        print(f"File exists: {dest_path} (Size: {size / 1024 / 1024:.2f} MB)")
        # Force re-download if it's the 500MB one and we want the 130MB one
        if size > 200 * 1024 * 1024 and "nomic" in str(dest_path):
             print("File is too large (>200MB), assuming it's the non-quantized version. Re-downloading quantized version...")
             dest_path.unlink()
        else:
             return

    print(f"Downloading {url} to {dest_path}...")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        if dest_path.exists():
            dest_path.unlink() # Remove partial file

def main():
    models_dir = Path("models")
    
    # 1. Nomic Embed Text v1.5 (Quantized ~137MB)
    nomic_dir = models_dir / "nomic-embed-text-v1.5"
    
    # Try to find the quantized version url.
    # Often named model_quantized.onnx in HF repo "onnx" folder.
    # Or sometimes the main model.onnx IS quantized if it's a specific "onnx" branch/repo.
    # Nomic AI official repo usually has both.
    # Let's try explicit quantized filename first, but save as model.onnx for RAE compatibility.
    
    # Standard Nomic ONNX repo often has: model.onnx (full), model_quantized.onnx (int8)
    nomic_quantized_url = "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/resolve/main/onnx/model_quantized.onnx"
    
    download_file(nomic_quantized_url, nomic_dir / "model.onnx")
    
    # 2. All-MiniLM-L6-v2 (Should be ~23MB)
    # Check if we have it
    minilm_dir = models_dir / "all-MiniLM-L6-v2"
    minilm_path = minilm_dir / "model.onnx"
    
    if not minilm_path.exists():
         print("Downloading All-MiniLM-L6-v2...")
         # Standard HF url for this model's ONNX
         minilm_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model.onnx"
         # Note: This might be the full one. Quantized is smaller.
         # The user said 23MB. The standard pytorch model is ~90MB. 
         # ONNX quantized is usually ~23MB.
         minilm_quantized_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model_quantized.onnx"
         
         # Try quantized first to match size constraint
         try:
             download_file(minilm_quantized_url, minilm_path)
         except:
             print("Quantized MiniLM not found, trying standard...")
             download_file(minilm_url, minilm_path)
    else:
         print(f"All-MiniLM-L6-v2 exists ({minilm_path.stat().st_size / 1024 / 1024:.2f} MB)")

    # 3. Third model? User mentioned 18MB. 
    # Could be `bge-micro`, `paraphrase-MiniLM-L3-v2` or similar small model.
    # Or maybe tokenizer files?
    # Without specific name, I'll stick to Nomic + MiniLM which covers the main requirements.

if __name__ == "__main__":
    main()