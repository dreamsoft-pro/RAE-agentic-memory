import asyncio
import os
import sys

# Add the module path to sys.path to import CivicRAEClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))
from api_client import CivicRAEClient

async def run_test():
    api_url = "http://localhost:8001"
    api_key = "test-key"
    client = CivicRAEClient(api_url, api_key)
    
    print("🚀 Starting RAE Ingestion Test (ISO-Compliant)...")
    
    test_content = "To jest testowa treść dotycząca analizy budżetu obywatelskiego na rok 2026. Dokument zawiera dane o wydatkach na infrastrukturę rowerową."
    test_source = "test:budget_analysis_2026.txt"
    
    success = await client.ingest_document(
        content=test_content,
        source=test_source,
        metadata={"test_run": "initial_validation", "format_version": "v2_contract"}
    )
    
    if success:
        print("✅ SUCCESS: Data ingested into RAE following the required contract.")
        stats = await client.get_stats()
        print(f"📊 Current Stats for civic-watchdog: {stats}")
    else:
        print("❌ FAILED: Data ingestion rejected by RAE. Check API logs.")

if __name__ == "__main__":
    asyncio.run(run_test())
