from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import structlog
import re
from datetime import datetime
from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.services.rae_core_service import RAECoreService
from apps.memory_api.industrial_bridge import ScreenWatcherBridge

router = APIRouter(prefix="/procedural", tags=["Procedural Oracle"])
logger = structlog.get_logger(__name__)

# LISTA PRAWDY (Mandatory Context)
SYSTEM_MACHINES = """
W systemie zarejestrowane są WYŁĄCZNIE 3 maszyny:
1. TrueJet1 (Kod: M01) - drukarka
2. TrueJet2 (Kod: M02) - drukarka
3. Kongsberg (Kod: K01) - ploter tnący
"""

class QueryRequest(BaseModel):
    query: str
    project: str = "default"

def extract_date(text):
    months = {"stycznia": "01", "lutego": "02", "marca": "03", "kwietnia": "04", "maja": "05", "czerwca": "06", "lipca": "07", "sierpnia": "08", "września": "09", "października": "10", "listopada": "11", "grudnia": "12"}
    text = text.lower()
    for name, num in months.items():
        if name in text:
            m = re.search(r'(\d{1,2})', text)
            if m: return f"2026-{num}-{m.group(1).zfill(2)}"
    m_iso = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if m_iso: return m_iso.group(1)
    return None

def extract_machine(text):
    text = text.upper()
    if "TRUEJET1" in text or "M01" in text: return "M01"
    if "TRUEJET2" in text or "M02" in text: return "M02"
    if "KONGSBERG" in text or "K01" in text: return "K01"
    return None

@router.post("/query")
async def query_procedural(
    request: QueryRequest,
    rae_service: RAECoreService = Depends(get_rae_core_service)
):
    try:
        bridge = ScreenWatcherBridge()
        target_date = extract_date(request.query)
        target_machine = extract_machine(request.query)
        
        industrial_context = ""
        # Always fetch some data if machine or date is mentioned
        if target_date or target_machine or "maszyn" in request.query.lower():
            # If no date, use today (Feb 19 according to system context)
            query_date = target_date or "2026-02-19"
            data = bridge.get_daily_performance(query_date)
            
            if target_machine:
                filtered = [d for d in data if d['code'] == target_machine]
                if filtered:
                    d = filtered[0]
                    industrial_context = f"\nRAPORT DLA MASZYNY {d['name']} ({d['code']}) Z DNIA {query_date}:\n- Średnia prędkość: {d['avg_speed_m2h']:.2f} m2/h\n- Maksymalna prędkość: {d['max_speed_m2h']:.2f} m2/h\n- Liczba odczytów: {d['odczyty']}"
                else:
                    industrial_context = f"\nBrak danych o wydajności dla {target_machine} w dniu {query_date}."
            else:
                lines = [f"- {d['name']} ({d['code']}): {d['avg_speed_m2h']:.2f} m2/h" for d in data]
                industrial_context = f"\nRAPORT WYDAJNOŚCI Z DNIA {query_date}:\n" + "\n".join(lines)

        # Search Memory
        results = await rae_service.engine.search_memories(query=request.query, tenant_id="default", project=request.project, top_k=5)
        
        from rae_core.context.builder import ContextBuilder
        builder = ContextBuilder(max_tokens=3000)
        memory_context, _ = builder.build_context(results, query=request.query)
        
        full_context = f"{SYSTEM_MACHINES}\n{memory_context}\n{industrial_context}"

        system_prompt = (
            "Jesteś Wyrocznią systemu ScreenWatcher. NIE WOLNO Ci zmyślać maszyn. "
            "W systemie są tylko 3 maszyny wymienione w sekcji WYŁĄCZNIE. "
            "Odpowiadaj na podstawie dostarczonego RAPORTU. Jeśli raport jest pusty, powiedz że nie widzę pracy w tym dniu. "
            "Odpowiadaj po polsku."
        )
        
        prompt = f"ZAPYTANIE: {request.query}\n\nKONTEKST:\n{full_context}"
        instruction = await rae_service.engine.generate_text(prompt=prompt, system_prompt=system_prompt)

        return {
            "instruction": instruction,
            "results": [{"content": r.get("content"), "layer": r.get("layer")} for r in results]
        }

    except Exception as e:
        logger.error("procedural_query_failed", error=str(e))
        return {"instruction": f"Błąd analizy: {str(e)}", "results": []}
