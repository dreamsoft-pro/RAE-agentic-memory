"""
Intelligence Test for RAE Theory Router and Fluid Dispatcher.
Verifies autonomous strategy switching based on query intent.
"""

import asyncio
import structlog
from uuid import uuid4
from rae_core.math.theories.registry import FluidDispatcher

# Configure logging to see the theory decisions
structlog.configure(
    processors=[structlog.processors.JSONRenderer()]
)

async def run_intelligence_test():
    dispatcher = FluidDispatcher(profile={"mode": "lite"})
    
    # Mock candidates
    candidates = [
        {"id": uuid4(), "score": 0.9, "metadata": {"importance": 0.8}, "content": "Error 0x8004 in production logs"},
        {"id": uuid4(), "score": 0.7, "metadata": {"importance": 0.5}, "content": "Architectural overview of the shopping cart system"}
    ]

    print("\n--- TEST 1: TECHNICAL PRECISE PATH ---")
    query_tech = "Fix error 0x8004 in CartService"
    # The router should detect symbols and pick ['stability', 'decay']
    results_tech = dispatcher.execute_cascade(candidates, query_tech)
    
    print("\n--- TEST 2: ABSTRACT DEEP PATH ---")
    query_abstract = "What are the long-term implications of using a monolithic architecture for a multi-tenant print shop system?"
    # The router should detect complexity/length and pick ['stability', 'decay', 'resonance']
    results_abstract = dispatcher.execute_cascade(candidates, query_abstract)

if __name__ == "__main__":
    asyncio.run(run_intelligence_test())
