import asyncio
import json
import os
import structlog
from rae_core.reflection.layers.coordinator import ReflectionCoordinator
from apps.memory_api.services.llm import get_llm_provider
from apps.memory_api.config import settings

# Configure logging to be visible
structlog.configure(
    processors=[structlog.processors.JSONRenderer()]
)

async def run_diagnostic():
    print("--- RAE L4 DIAGNOSTIC START ---")
    
    # 1. Component Init
    print("1. Initializing LLM Provider...")
    llm = get_llm_provider(settings)
    
    print(f"2. Initializing Coordinator (Strategy: {settings.RAE_REFLECTION_STRATEGY})...")
    coord = ReflectionCoordinator(
        strategy=settings.RAE_REFLECTION_STRATEGY,
        llm_provider=llm,
        llm_model=settings.RAE_LLM_MODEL_DEFAULT
    )
    
    # 3. Payload Mock (Simulating a real decision)
    payload = {
        "analysis": "Agent decided to refactor the database schema to improve performance.",
        "retrieved_sources_content": [
            "Source A: DB Schema is currently slow on joins.",
            "Source B: Indexing column X improves speed by 40%."
        ],
        "retrieved_sources": ["uuid-1", "uuid-2"], # L1 requires this field
        "decision": "refactor_schema",
        "confidence": 0.95,
        "metadata": {"project": "diagnostic_test"}
    }
    
    print(f"3. Running Reflections (Model: {settings.RAE_LLM_MODEL_DEFAULT})...")
    print("This may take a while if running on CPU. Watching for timeouts...")
    
    try:
        # We run ONLY reflections without storing, to isolate the LLM call
        result = await coord.run_reflections(payload)
        
        print("\n--- DIAGNOSTIC RESULT ---")
        print(json.dumps(result, indent=2))
        
        if result["l4_cognitive"].get("status") == "success":
            print("\n✅ SUCCESS: L4 Sage synthesized a lesson!")
        else:
            print(f"\n❌ FAILURE: L4 returned status: {result['l4_cognitive'].get('status')}")
            print(f"Reason: {result['l4_cognitive'].get('reason')}")
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
