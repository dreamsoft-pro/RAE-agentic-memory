from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import structlog
import re
import json
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
        
        # 1. Wyciąganie parametrów
        parsing_prompt = (
            f"Z pytania: '{request.query}' wyciągnij: start_date, end_date, start_hour, end_hour, machine.\n"
            "ZAKŁADAJ ROK 2026. Zwróć TYLKO JSON."
        )
        params_raw = await rae_service.engine.generate_text(prompt=parsing_prompt, system_prompt="Parser parametrów.")
        try:
            p = json.loads(re.search(r'(\{.*\})', params_raw).group(1))
        except:
            p = {"start_date": None, "end_date": None, "start_hour": None, "end_hour": None, "machine": None}

        # 2. Buduj SQL z FILTREM REALIZMU (Max 450 m2/h)
        where = ["r.name = 'real_speed_m2h'", "r.value < 450"] # Odrzucamy błędy OCR
        if p.get("start_date") and p.get("end_date"):
            where.append(f"DATE(r.timestamp) BETWEEN '{p['start_date']}' AND '{p['end_date']}'")
        if p.get("start_hour") is not None and p.get("end_hour") is not None:
            where.append(f"HOUR(r.timestamp) BETWEEN {p['start_hour']} AND {p['end_hour']}")
        if p.get("machine"):
            where.append(f"m.code = '{p['machine']}'")
        
        sql = f"SELECT m.code, m.name, AVG(r.value) as avg_speed, MAX(r.value) as max_speed FROM collector_metricreading r JOIN registry_machine m ON r.machine_id = m.id WHERE {' AND '.join(where)} GROUP BY m.code, m.name"
        
        db_result = bridge.execute_query(sql)

        # 3. Finalna odpowiedź z zakazem zmyślania wielkich liczb
        final_prompt = (
            f"PYTANIE: {request.query}\nWYNIK BAZY: {str(db_result)}\n"
            "Podaj średnią i maksymalną prędkość. Jednostka to m2/h. "
            "UWAGA: Maksymalna wydajność maszyny to 400 m2/h. Jeśli w WYNIK BAZY widzisz większe liczby, zignoruj je. "
            "Jeśli dane są puste, powiedz że brak odczytów."
        )
        
        raw_answer = await rae_service.engine.generate_text(prompt=final_prompt, system_prompt="Jesteś Silicon Oracle. Podajesz tylko REALNE liczby z bazy.")

        return {
            "instruction": raw_answer,
            "debug": {"parsed": p, "db_raw": db_result}
        }

    except Exception as e:
        logger.error("procedural_query_failed", error=str(e))
        return {"instruction": f"Błąd: {str(e)}", "results": []}
