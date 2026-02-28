"""
Script to ingest real machine logs from TrueJet2 into RAE.
Uses the Universal Ingest Pipeline (System 46.1) with AFE and valid UUIDs.
"""

import os
import json
import asyncio
import sys
from pathlib import Path
import structlog
from uuid import UUID

# Add project root and rae-core to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_core.engine import RAEEngine
from rae_adapters.postgres import PostgreSQLStorage
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider

# Configure logging
structlog.configure()
logger = structlog.get_logger()

async def main():
    # Setup Engine
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_url = f"http://{qdrant_host}:6333"
    
    storage = PostgreSQLStorage(db_url)
    vector_store = QdrantVectorStore(url=qdrant_url)
    
    # Use native ONNX provider (System 2.0)
    model_dir = "/app/models/all-MiniLM-L6-v2"
    embedding_provider = NativeEmbeddingProvider(
        model_path=f"{model_dir}/model.onnx",
        tokenizer_path=f"{model_dir}/tokenizer.json"
    )
    
    engine = RAEEngine(
        memory_storage=storage, 
        vector_store=vector_store,
        embedding_provider=embedding_provider
    )
    
    log_file = "benchmarking/sets/truejet_real_logs.jsonl"
    if not os.path.exists(log_file):
        print(f"File not found: {log_file}")
        return

    print(f"🚀 Ingesting TrueJet logs from {log_file}...")
    
    # VALID UUIDs are mandatory for the database
    # Based on earlier db_stats, I'll use a standard test tenant ID if available, 
    # or generate a consistent one for this analysis.
    tenant_id = "c7408c32-198c-41d2-a0ab-6909cd8df89e" 
    agent_id = "00000000-0000-0000-0000-000000000001"
    
    with open(log_file, "r") as f:
        count = 0
        success_count = 0
        for line in f:
            try:
                data = json.loads(line)
                timestamp = data.get("timestamp")
                metrics = data.get("metrics", {})
                content = metrics.get("pole_1", "")
                
                if not content: continue
                
                # Ingest into RAE
                m_id = await engine.store_memory(
                    content=content,
                    source="truejet_physical_log",
                    project="TJ02_ANALYSIS",
                    tenant_id=tenant_id,
                    agent_id=agent_id,
                    metadata={
                        "machine": "TrueJet2",
                        "raw_timestamp": timestamp,
                        "ingest_type": "machine_telemetry"
                    }
                )
                
                if m_id:
                    success_count += 1
                
                count += 1
                if success_count % 50 == 0 and success_count > 0:
                    print(f"Stored {success_count} memory points...")
                    
            except Exception as e:
                # print(f"Error at line {count}: {e}")
                pass
                
    print(f"✅ Finished. Ingested {success_count} memories.")

if __name__ == "__main__":
    asyncio.run(main())
