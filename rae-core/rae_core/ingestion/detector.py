"""
RAE Content Signature Detector (UICTC).
Stage 2: S-D-O Layer Analysis.
"""

import math
import re
from collections import Counter
from typing import Any, Dict, List
from .interfaces import ISignatureDetector, ContentSignature, IngestAudit

class ContentSignatureDetector(ISignatureDetector):
    """
    Calculates structural and distributional signatures of the input.
    """
    
    def detect(self, text: str) -> tuple[ContentSignature, IngestAudit]:
        # 1. Structural Analysis (S-Layer)
        struct = self._analyze_structure(text)
        
        # 2. Distributional Analysis (D-Layer)
        dist = self._analyze_distribution(text, struct)
        
        # 3. Stability Analysis (O-Layer)
        stab = self._analyze_stability(text, struct, dist)
        
        signature = ContentSignature(struct=struct, dist=dist, stab=stab)
        
        audit = IngestAudit(
            stage="detect",
            action="signature_generation",
            trace={
                "mode_detected": struct["mode"],
                "entropy": dist["token_entropy"]
            }
        )
        
        return signature, audit

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        line_count = len(lines)
        if line_count == 0: return {"mode": "EMPTY"}
        
        avg_line_len = sum(len(l) for l in lines) / line_count
        
        # Ratios
        digit_count = sum(c.isdigit() for c in text)
        upper_count = sum(c.isupper() for c in text)
        special_count = sum(not c.isalnum() and not c.isspace() for c in text)
        
        total_chars = len(text) or 1
        
        # Markers (using stripped lines for better precision)
        time_markers = len(re.findall(r'\d{2,4}[-:/]\d{2}[-:/]\d{2,4}', text))
        # List markers: Krok X, Step X, 1., -, * at start of line
        list_markers = sum(1 for l in lines if re.match(r'^(?:Krok|Step|Kolejno|\d+[\.)]|[-*•])', l, re.I))
        identifiers = len(re.findall(r'\b[A-Z0-9]{3,}[-_][A-Z0-9]{2,}\b', text))
        
        # Table-like check (pipes or multiple spaces INSIDE line)
        table_markers = sum(1 for l in lines if '|' in l or re.search(r'\w{2,} {3,}\w{2,}', l))
        
        # Determine Mode (Dominance rules)
        mode = "PROSE_PARAGRAPH_LIKE"
        
        # Priority 1: Logs
        if line_count > 5 and (time_markers / line_count) > 0.4:
            mode = "LINEAR_LOG_LIKE"
        # Priority 2: Procedures
        elif (list_markers / line_count) > 0.3:
            mode = "LIST_PROCEDURE_LIKE"
        # Priority 3: Tables
        elif (table_markers / line_count) > 0.4:
            mode = "TABLE_RECORD_LIKE"
        # Priority 4: Tech Specs
        elif identifiers > (line_count / 2):
            mode = "TECHNICAL_SPEC_LIKE"
            
        return {
            "mode": mode,
            "line_count": line_count,
            "avg_line_len": round(avg_line_len, 1),
            "digit_ratio": round(digit_count / total_chars, 3),
            "special_ratio": round(special_count / total_chars, 3),
            "upper_ratio": round(upper_count / total_chars, 3),
            "markers": {
                "time": time_markers,
                "list": list_markers,
                "table": table_markers,
                "id": identifiers
            }
        }

    def _analyze_distribution(self, text: str, struct: Dict[str, Any]) -> Dict[str, Any]:
        words = text.split()
        if not words: return {"token_entropy": 0}
        
        # Shannon Entropy
        counts = Counter(words)
        total = len(words)
        entropy = -sum((count/total) * math.log2(count/total) for count in counts.values())
        
        # Repeatability (How many lines start the same?)
        lines = [l.strip()[:10] for l in text.split('\n') if len(l.strip()) > 10]
        if lines:
            line_prefixes = Counter(lines)
            repeatability = sum(count for count in line_prefixes.values() if count > 1) / len(lines)
        else:
            repeatability = 0.0
            
        return {
            "token_entropy": round(entropy, 3),
            "repeatability_score": round(repeatability, 3),
            "vocab_size": len(counts)
        }

    def _analyze_stability(self, text: str, struct: Dict[str, Any], dist: Dict[str, Any]) -> Dict[str, Any]:
        # Logic conflicts: high repeatability but high entropy? 
        conflict = False
        if struct.get("mode") == "LINEAR_LOG_LIKE" and dist.get("token_entropy", 0) > 8.0:
            conflict = True
            
        return {
            "conflict": conflict,
            "order_sensitive": struct.get("mode") in ["LINEAR_LOG_LIKE", "LIST_PROCEDURE_LIKE"]
        }
