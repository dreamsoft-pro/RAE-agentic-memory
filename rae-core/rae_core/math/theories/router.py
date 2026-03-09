"""
Theory Router - Autonomous selection of mathematical strategies.
Analyzes query signature and intent to decide the fluid flow of theories.
Zero Regression: Performance optimization without loss of intelligence.
"""

import structlog
from typing import Any, List, Dict
from rae_core.math.features_v2 import FeatureExtractorV2

logger = structlog.get_logger(__name__)

class TheoryRouter:
    """
    Decides the sequence of mathematical theories based on content intent.
    Ensures that even on Lite environments, the best strategy is used.
    """
    
    def __init__(self):
        self.extractor = FeatureExtractorV2()
        
    def decide_sequence(self, query: str, profile: Dict[str, Any]) -> List[str]:
        """
        Returns a sequence of theory names tailored to the query depth.
        """
        features = self.extractor.extract(query)
        
        # 1. Technical/Exact Intent -> Precise Flow
        # Filter symbols: only count those that look like codes or identifiers (e.g. 0x, _, IDs)
        technical_symbols = [s for s in features.symbols if len(s) > 3 or "0x" in s or "_" in s]
        
        if technical_symbols:
            logger.info("theory_route_selected", path="precise_technical", symbols=len(technical_symbols))
            return ["stability", "decay"] 
            
        # 2. Reasoning/Architectural Intent -> Deep Manifold Flow
        # High complexity or very long queries trigger the full resonance 'waterfall'.
        if features.query_complexity > 0.4 or len(query.split()) > 12:
            logger.info("theory_route_selected", path="deep_manifold")
            return ["stability", "decay", "resonance"]
            
        # 3. Default/Conversation Intent -> Semantic Flow
        # Standard flow for general queries.
        return ["stability", "decay"]
