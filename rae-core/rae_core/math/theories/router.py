"""
Theory Router (Tesla 3-6-9 Edition).
Decides the sequence of mathematical theories based on 9 cognitive domains.
"""

import structlog
import json
import os
from typing import Any, List, Dict
from rae_core.math.features_v2 import FeatureExtractorV2
from .atlas import DOMAINS

logger = structlog.get_logger(__name__)

class TheoryRouter:
    """
    Cognitive Router that maps query signatures to 3-6-9 Domain Profiles.
    Evolves through theory_genome.json.
    """
    
    def __init__(self):
        self.extractor = FeatureExtractorV2()
        self.genome_path = os.path.join(os.path.dirname(__file__), "theory_genome.json")
        
    def _get_evolved_sequence(self, domain: str, default: List[str]) -> List[str]:
        if os.path.exists(self.genome_path):
            try:
                with open(self.genome_path, "r") as f:
                    genome = json.load(f)
                    return genome.get("domains", {}).get(domain, {}).get("sequence", default)
            except:
                pass
        return default

    def decide_sequence(self, query: str, profile: Dict[str, Any]) -> List[str]:
        """
        Returns a sequence of theory names tailored to detected query characteristics.
        """
        features = self.extractor.extract(query)
        
        # 1. Hard Industrial Detection (Deterministyczny Skalpel)
        if features.is_industrial or features.symbols:
            logger.info("theory_route_selected", domain="industrial", symbols=len(features.symbols))
            return self._get_evolved_sequence("industrial", DOMAINS["industrial"])
            
        # 2. Quantitative/Analytical Detection
        if features.is_quantitative:
            logger.info("theory_route_selected", domain="it_support")
            return self._get_evolved_sequence("it_support", DOMAINS["it_support"])
            
        # 3. High Complexity / Abstract Intent (Semantic Manifold)
        if features.query_complexity > 0.6:
            logger.info("theory_route_selected", domain="scientific")
            return DOMAINS["scientific"]
            
        # 4. Default: Semantic Flow
        logger.info("theory_route_selected", domain="personal")
        return DOMAINS["personal"]
