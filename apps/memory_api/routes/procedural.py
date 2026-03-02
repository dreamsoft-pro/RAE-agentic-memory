from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import structlog
import re
import json
from datetime import datetime
from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.services.rae_core_service import RAECoreService
from apps.memory_api.industrial_bridge import ScreenWatcherBridge

router = APIRouter(prefix="/procedural", tags=["Procedural Oracle"])
logger = structlog.get_logger(__name__)

class QueryRequest(BaseModel):
    query: str
    project: str = "default"

@router.post("/query")
async def query_procedural(
    request: QueryRequest,
    rae_service: RAECoreService = Depends(get_rae_core_service)
):
    try:
        bridge = ScreenWatcherBridge()
        
        # 1. Wyciąganie parametrów przez LLM
        parsing_prompt = (
            f"Z pytania: '{request.query}' wyciągnij: date (YYYY-MM-DD) i machine (M01, M02, K01).\n"
            "ZAKŁADAJ ROK 2026. Zwróć TYLKO JSON."
        )
        params_raw = await rae_service.engine.generate_text(prompt=parsing_prompt, system_prompt="Parser parametrów.")
        try:
            p = json.loads(re.search(r'(\{.*\})', params_raw).group(1))
        except:
            p = {"date": "2026-02-18", "machine": "M01"} # Fallback

        # 2. POBIERANIE SMART METRYK (Logika z Grafany)
        db_result = bridge.get_smart_metrics(p.get("machine", "M01"), p.get("date", "2026-02-18"))

        # Konwersja Decimal na float dla modelu LLM
        if isinstance(db_result, list) and len(db_result) > 0:
            for k, v in db_result[0].items():
                if hasattr(v, '__float__'): db_result[0][k] = float(v)

        # 3. Finalna odpowiedź
        final_prompt = (
            f"PYTANIE: {request.query}\n"
            f"DANE OEE Z BAZY (LOGIKA GRAFANY): {str(db_result)}\n"
            "Odpowiedz po polsku. Używaj pojęć: 'Wydajność Netto' (podczas pracy), 'Mikroprzestoje' (sumarycznie w minutach), 'Przerwy' (powyżej 5 min). "
            "Bądź bardzo precyzyjny co do liczb. Jednostka wydajności to m2/h."
        )
        
        raw_answer = await rae_service.engine.generate_text(prompt=final_prompt, system_prompt="Jesteś Ekspertem OEE Silicon Oracle.")

        return {
            "instruction": raw_answer,
            "debug": {"parsed": p, "db_raw": db_result}
        }

    except Exception as e:
        logger.error("procedural_query_failed", error=str(e))
        return {"instruction": f"Błąd analizy: {str(e)}", "results": []}
