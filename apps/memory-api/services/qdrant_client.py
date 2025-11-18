import uuid
import os
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

def hybrid_search(query_text: str, k: int, filters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    # TODO: implementacja realna (dense + sparse + RRF)
    return []

import psycopg2
from datetime import datetime

qdrant_client = QdrantClient(host=os.environ.get("QDRANT_HOST", "localhost"), port=6333)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def _get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRE_HOST", "localhost"),
        dbname=os.environ.get("POSTGRES_DB", "memory"),
        user=os.environ.get("POSTGRES_USER", "memory"),
        password=os.environ.get("POSTGRES_PASSWORD", "example")
    )

def add_memory_vectorized(payload: Dict[str, Any]) -> str:
    memory_id = str(uuid.uuid4())
    vector = embedding_model.encode(payload["content"]).tolist()

    qdrant_client.upsert(
        collection_name="memories",
        points=[
            models.PointStruct(
                id=memory_id,
                vector=vector,
                payload=payload
            )
        ]
    )

    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SET app.tenant_id = %s", (payload["tenant_id"],))
    cursor.execute(
        "INSERT INTO memories (memory_id, tenant_id, agent_id, memory_type, content, source_id, created_at, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (memory_id, payload["tenant_id"], payload["agent_id"], payload["memory_type"], payload["content"], payload.get("source_id"), payload.get("created_at", datetime.now()), payload.get("metadata"))
    )
    conn.commit()
    cursor.close()
    conn.close()

    return memory_id
