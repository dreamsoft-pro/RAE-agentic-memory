import yaml
import httpx
import os
import asyncio
from pathlib import Path

API_URL = os.getenv("RAE_API_URL", "http://localhost:8001/v2/memories/")
HEADERS = {"X-API-Key": "test-key", "X-Tenant-Id": "00000000-0000-0000-0000-000000000000"}

async def ingest_atlas():
    # Adjusted path to match reality
    atlas_path = Path(__file__).parent.parent / "rae_core" / "rae_core" / "contracts" / "global_atlas.yaml"
    if not atlas_path.exists():
        print(f"❌ Atlas not found at {atlas_path}")
        return

    with open(atlas_path, "r") as f:
        data = yaml.safe_load(f)

    print(f"🚀 Ingesting {len(data['contracts'])} contracts into RAE...")

    async with httpx.AsyncClient() as client:
        for contract in data["contracts"]:
            content = f"CONTRACT {contract['id']}: {contract['name']}\n{contract['description']}"
            payload = {
                "content": content,
                "layer": "semantic",
                "tags": ["global_contract", f"level_{contract['level']}", contract["type"]],
                "metadata": contract
            }
            try:
                resp = await client.post(API_URL, json=payload, headers=HEADERS)
                if resp.status_code in [200, 201]:
                    print(f"✅ Ingested: {contract['id']}")
                else:
                    print(f"⚠️ Failed {contract['id']}: {resp.status_code} - {resp.text}")
            except Exception as e:
                print(f"❌ Error ingesting {contract['id']}: {e}")

if __name__ == "__main__":
    asyncio.run(ingest_atlas())
