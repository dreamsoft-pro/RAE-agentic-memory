# Placeholder klienta Qdrant (hybrydowe zapytanie dense+sparse + RRF)
# Docelowo użyj qdrant-client i Universal Query API.
from typing import List, Dict, Any

def hybrid_search(query_text: str, k: int, filters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    # TODO: implementacja realna (dense + sparse + RRF)
    return []

def add_memory_vectorized(payload: Dict[str, Any]) -> str:
    # TODO: embed + insert do Qdrant + zapis metadanych
    return "00000000-0000-0000-0000-000000000000"
