import asyncio
import time

import httpx

OLLAMA_URL = "http://localhost:11434/api"

async def test_generation():
    print("🚀 Starting text generation (deepseek-coder:1.3b)...")
    start = time.time()
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{OLLAMA_URL}/generate", json={
            "model": "deepseek-coder:1.3b",
            "prompt": "Summarize the importance of memory in autonomous agents in 3 sentences.",
            "stream": False
        })
        duration = time.time() - start
        print(f"✅ Generation completed in {duration:.2f}s")
        return resp.json()

async def test_embedding():
    print("🚀 Starting embedding generation (nomic-embed-text)...")
    start = time.time()
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{OLLAMA_URL}/embeddings", json={
            "model": "nomic-embed-text",
            "prompt": "Memory consistency is key to reliability."
        })
        duration = time.time() - start
        print(f"✅ Embedding completed in {duration:.2f}s")
        return resp.json()

async def check_ps():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{OLLAMA_URL}/ps")
        print("\n--- Current Models in VRAM ---")
        print(resp.text)

async def main():
    print("🧪 Running Concurrent Model Test on Node 3...")

    # Run both simultaneously
    results = await asyncio.gather(
        test_generation(),
        test_embedding()
    )

    # Check what is loaded in VRAM
    await check_ps()

if __name__ == "__main__":
    asyncio.run(main())
