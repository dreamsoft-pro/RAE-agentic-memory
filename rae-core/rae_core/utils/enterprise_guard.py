# rae_core/utils/enterprise_guard.py
import os
import time
import psutil
import logging
from functools import wraps
from typing import Callable, Any
from datetime import datetime

# Import z naszego nowego mostka
from rae_core.utils.memory_bridge import RAEMemoryBridge
from rae_core.utils.context import RAEContextLocator

class FatalEnterpriseError(Exception):
    """Wyrzucany, gdy moduł łamie twardy kontrakt ISO 27000 lub Telemetrii."""
    pass

class RAE_Enterprise_Foundation:
    """Twardy kontrakt dla każdego modułu RAE-Suite."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = logging.getLogger(f"RAE.Enterprise.{module_name}")
        self.bridge = RAEMemoryBridge(project_name=module_name)
        self._enforce_iso27000_compliance()

    def _enforce_iso27000_compliance(self):
        """Weryfikuje środowisko startowe."""
        # 1. Sprawdzenie izolacji (Nie powinieneś działać jako root, jeśli to nie jest absolutnie konieczne)
        if hasattr(os, 'geteuid') and os.geteuid() == 0 and self.module_name not in ["rae-hive", "rae-quality"]:
            self.logger.warning("ISO 27001 Violation: Process is running as root. This is a severe security risk.")
            # W przyszłości tu będzie podnoszony wyjątek FatalEnterpriseError
        
        # 2. Sprawdzenie telemetrii
        if not os.getenv("RAE_API_URL"):
            raise FatalEnterpriseError(f"[{self.module_name}] RAE_API_URL missing. Telemetry and Audit cannot function.")
            
        # 3. Sprawdzenie tożsamości
        tenant = RAEContextLocator.get_current_tenant_id()
        if tenant == "UNKNOWN_TENANT" or tenant == "00000000-0000-0000-0000-000000000000":
            self.logger.warning(f"[{self.module_name}] Running under Default Tenant. Strict auditing may fail.")

def audited_operation(operation_name: str, impact_level: str = "medium"):
    """
    Dekorator (Twardy Kontrakt). Zmusza każdą funkcję do:
    1. Zalogowania startu (Audit Trail).
    2. Zmierzenia czasu i zasobów (Telemetry).
    3. Zaraportowania wyniku do Pamięci.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            return await _execute_with_audit(self, func, operation_name, impact_level, *args, **kwargs)
            
        @wraps(func)
        def sync_wrapper(self, *args, **kwargs) -> Any:
            return _execute_with_audit(self, func, operation_name, impact_level, *args, **kwargs)

        import asyncio
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    def _execute_with_audit(self_instance, func, op_name, impact, *args, **kwargs):
        # Sprawdzamy czy klasa korzysta z Enterprise Foundation
        if not hasattr(self_instance, 'enterprise_foundation'):
            raise FatalEnterpriseError(f"Class {self_instance.__class__.__name__} must implement RAE_Enterprise_Foundation to use audited operations.")
            
        foundation: RAE_Enterprise_Foundation = self_instance.enterprise_foundation
        
        # Metryki startowe
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_start = process.memory_info().rss
        
        # Audit: Start
        audit_meta = {
            "operation": op_name,
            "impact": impact,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "started",
            "args": str(args), # Wymaga sanityzacji PII w przyszłości
        }
        foundation.bridge.save_event(
            content=f"Initiated: {op_name}",
            human_label=f"Audit: {op_name}",
            metadata=audit_meta
        )

        try:
            # Wykonanie
            result = func(self_instance, *args, **kwargs)
            status = "success"
            return result
        except Exception as e:
            status = "failed"
            foundation.logger.error(f"Operation {op_name} failed: {e}")
            raise e
        finally:
            # Metryki końcowe
            duration = time.time() - start_time
            mem_used = process.memory_info().rss - mem_start
            
            # Audit: Zakończenie + Telemetria
            final_meta = {
                "operation": op_name,
                "status": status,
                "duration_seconds": round(duration, 4),
                "memory_delta_bytes": mem_used,
                "category": "security_audit"
            }
            foundation.bridge.save_event(
                content=f"Completed: {op_name} with status {status}. Took {duration:.2f}s.",
                human_label=f"Telemetry: {op_name}",
                metadata=final_meta
            )
            
    return decorator
