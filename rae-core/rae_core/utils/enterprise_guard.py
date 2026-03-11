# rae_core/utils/enterprise_guard.py
import os
import time
import psutil
import logging
from functools import wraps
from typing import Callable, Any, Optional
from datetime import datetime

from rae_core.utils.memory_bridge import RAEMemoryBridge
from rae_core.utils.context import RAEContextLocator

class FatalEnterpriseError(Exception):
    """Raised when an Enterprise Contract is violated."""
    pass

class RAE_Enterprise_Foundation:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = logging.getLogger(f"RAE.Enterprise.{module_name}")
        self.bridge = RAEMemoryBridge(project_name=module_name)

def audited_operation(operation_name: str, impact_level: str = "medium"):
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
        if not hasattr(self_instance, 'enterprise_foundation'):
            raise FatalEnterpriseError(f"Class {self_instance.__class__.__name__} must implement RAE_Enterprise_Foundation.")
            
        foundation: RAE_Enterprise_Foundation = self_instance.enterprise_foundation
        
        # Wyciąganie informacji o modelu LLM z kwargs (jeśli agent go podał)
        llm_model = kwargs.get("llm_model") or os.getenv("DEFAULT_LLM_MODEL", "unknown-model")
        
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_start = process.memory_info().rss
        
        # Intelligent Labeling: Tworzymy czytelną etykietę jeśli nie podano
        op_label = f"[{foundation.module_name.upper()}] Operation: {op_name.replace('_', ' ').title()}"
        
        # Audit: Intent with Source Tracking
        audit_meta = {
            "operation": op_name,
            "source_module": foundation.module_name,
            "llm_model": llm_model,
            "impact": impact,
            "status": "started",
            "timestamp": datetime.utcnow().isoformat()
        }
        foundation.bridge.save_event(
            content=f"Operation {op_name} started by {foundation.module_name} using {llm_model}",
            human_label=f"{op_label} (START)",
            metadata=audit_meta
        )

        try:
            # Tu właściwe wykonanie
            import asyncio
            if asyncio.iscoroutinefunction(func):
                result = func(self_instance, *args, **kwargs)
            else:
                result = func(self_instance, *args, **kwargs)
            status = "success"
            return result
        except Exception as e:
            status = "failed"
            foundation.bridge.save_event(
                content=f"CRITICAL FAILURE in {op_name}: {str(e)}",
                human_label=f"{op_label} (ALERT: FAILED)",
                metadata={"status": "error", "error": str(e), "category": "security_alert"}
            )
            raise e
        finally:
            duration = time.time() - start_time
            mem_used = (psutil.Process(os.getpid()).memory_info().rss - mem_start) / 1024 / 1024
            
            # Final Telemetry with LLM data
            foundation.bridge.save_event(
                content=f"Summary: {op_name} finished. Duration: {duration:.2f}s. Memory: {mem_used:.2f}MB.",
                human_label=f"{op_label} (TELEMETRY: SUCCESS)",
                metadata={
                    "operation": op_name,
                    "source_module": foundation.module_name,
                    "llm_model": llm_model,
                    "duration_s": duration,
                    "mem_delta_mb": mem_used,
                    "category": "performance_metrics"
                }
            )
            
    return decorator
