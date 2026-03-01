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
    nomic_quantized_url = "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/resolve/main/onnx/model_quantized.onnx"
    download_file(nomic_quantized_url, nomic_dir / "model.onnx")
    
    # Nomic Tokenizer
    nomic_tokenizer_url = "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/resolve/main/tokenizer.json"
    download_file(nomic_tokenizer_url, nomic_dir / "tokenizer.json")
    
    # 2. All-MiniLM-L6-v2
    minilm_dir = models_dir / "all-MiniLM-L6-v2"
    minilm_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model.onnx"
    minilm_quantized_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model_quantized.onnx"
    
    try:
        download_file(minilm_quantized_url, minilm_dir / "model.onnx")
    except:
        download_file(minilm_url, minilm_dir / "model.onnx")
        
    # MiniLM Tokenizer
    minilm_tokenizer_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer.json"
    download_file(minilm_tokenizer_url, minilm_dir / "tokenizer.json")

    # 3. Cross-Encoder (Neural Scalpel)
    # Model: ms-marco-MiniLM-L-6-v2
    ce_dir = models_dir / "cross-encoder"
    ce_model_url = "https://huggingface.co/Xenova/ms-marco-MiniLM-L-6-v2/resolve/main/onnx/model.onnx"
    ce_quantized_url = "https://huggingface.co/Xenova/ms-marco-MiniLM-L-6-v2/resolve/main/onnx/model_quantized.onnx"
    ce_tokenizer_url = "https://huggingface.co/Xenova/ms-marco-MiniLM-L-6-v2/resolve/main/tokenizer.json"

    try:
        download_file(ce_quantized_url, ce_dir / "model.onnx")
    except:
        download_file(ce_model_url, ce_dir / "model.onnx")
        
    download_file(ce_tokenizer_url, ce_dir / "tokenizer.json")

if __name__ == "__main__":
    main()