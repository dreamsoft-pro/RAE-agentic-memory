# rae_core/utils/context.py
import os
import json
import logging

class RAEContextLocator:
    """Intelligently detects project and tenant context based on environment and filesystem."""
    
    TENANT_MAP = {
        "screenwatcher_project": "66435998-b1d9-5521-9481-55a9fd10e014",
        "billboard-marker": "67694908-0b76-58a9-979d-3db20071e34a",
        "RAE-Suite": "00000000-0000-0000-0000-000000000000" # System level
    }

    @staticmethod
    def get_current_tenant_id():
        # 1. Sprawdzamy zmienną środowiskową (najwyższy priorytet)
        env_id = os.getenv("RAE_TENANT_ID")
        if env_id: return env_id
        
        # 2. Inteligentna detekcja po folderze projektu
        cwd = os.getcwd()
        for folder, uuid in RAEContextLocator.TENANT_MAP.items():
            if folder in cwd:
                return uuid
        
        # 3. Sprawdzamy czy istnieje plik .rae_context w folderze /projects (dla kontenerów)
        try:
            if os.path.exists("/projects/.rae_context"):
                with open("/projects/.rae_context", 'r') as f:
                    return f.read().strip()
        except: pass

        return "UNKNOWN_TENANT"

    @staticmethod
    def get_project_name():
        return os.getenv("RAE_PROJECT_NAME", "unnamed_production_module")
