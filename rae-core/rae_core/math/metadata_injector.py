import re
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class MetadataInjector:
    """
    Enriches query or document text with synonyms and parent entities 
    to close the semantic gap in models like TinyBERT.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        # Default industrial synonyms for benchmarking
        self.synonyms = {
            # MES / Production
            "mes": ["manufacturing execution system", "production system", "factory control", "shop floor", "oee"],
            "production": ["manufacturing", "line", "assembly", "output", "throughput", "mes"],
            "machine": ["equipment", "asset", "tool", "station", "automation"],
            "scada": ["automation", "control", "plc", "monitoring", "industrial control"],
            "downtime": ["stoppage", "stalled", "breakdown", "failure", "maintenance"],
            
            # ERP / Logistics / Finance
            "logistics": ["shipping", "transport", "warehouse", "delivery", "inventory", "supply chain"],
            "inventory": ["stock", "warehouse", "sku", "parts", "availability"],
            "payment": ["billing", "invoice", "transaction", "finance", "payment processor"],
            "invoice": ["billing", "payment", "erp", "accounting"],
            "customer": ["client", "account", "user", "tenant"],
            "pricing": ["cost", "contract", "billing", "subscription"],
            
            # Infrastructure / Tech Stack
            "postgres": ["database", "sql", "rdbms", "db", "storage"],
            "db": ["database", "sql", "postgres", "rdbms", "data store"],
            "database": ["db", "sql", "postgres", "storage", "rdbms"],
            "redis": ["cache", "kv-store", "nosql", "in-memory"],
            "disk": ["storage", "capacity", "space", "infrastructure", "hard drive"],
            "pool": ["resource", "exhausted", "limit", "capacity", "connections"],
            
            # Auth / Security
            "sso": ["authentication", "auth", "login", "identity", "saml", "oidc"],
            "auth": ["authentication", "login", "sso", "identity"],
            "authentication": ["auth", "login", "sso", "identity"],
            "security": ["vulnerability", "patch", "protection", "firewall", "cve"],
            "vulnerability": ["security bug", "exploit", "cve", "patch", "flaw"],
            
            # Incident / Operations
            "bug": ["issue", "error", "failure", "defect", "fault", "incident"],
            "error": ["bug", "issue", "failure", "fault", "500", "timeout", "exception"],
            "failure": ["bug", "issue", "error", "fault", "crash", "incident"],
            "crash": ["failure", "bug", "stopped", "down", "exception"],
            "performance": ["slow", "latency", "lag", "speed", "throughput"],
            "slow": ["performance", "latency", "lag", "speed", "sluggish"],
            "urgent": ["critical", "high priority", "asap", "emergency", "blocker"],
            "critical": ["urgent", "high priority", "emergency", "blocker", "p0"],
            "outage": ["down", "stopped", "interruption", "failure", "offline"],
            "latency": ["slow", "lag", "delay", "response time"],
            "slo": ["slos", "sla", "service level", "reliability", "metrics"],
        }
        # Expand with config synonyms if provided
        if "synonyms" in self.config:
            self.synonyms.update(self.config["synonyms"])

    def enrich_text(self, text: str) -> str:
        """Injects synonyms into the text."""
        if not text:
            return text

        text_lower = text.lower()
        found_synonyms = []

        # Optimization: split words to avoid heavy regex if text is large
        # but for small metadata injection regex is safer for boundaries
        for key, syns in self.synonyms.items():
            if key in text_lower: # Fast pre-check
                if re.search(rf"\b{re.escape(key)}s?\b", text_lower): # Match word and optional plural
                    found_synonyms.extend(syns)

        if not found_synonyms:
            return text

        # Append unique synonyms at the end to keep original text intact for reranker
        unique_syns = []
        for s in found_synonyms:
            if s not in unique_syns and s not in text_lower:
                unique_syns.append(s)

        if not unique_syns:
            return text

        enriched = f"{text} {' '.join(unique_syns)}"
        return enriched

    def process_query(self, query: str) -> str:
        return self.enrich_text(query)

    def process_document(self, text: str) -> str:
        return self.enrich_text(text)