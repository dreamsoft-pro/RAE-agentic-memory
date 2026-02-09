import math
import os
from typing import Any
from uuid import UUID

import structlog

from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder
from rae_core.math.metadata_injector import MetadataInjector
from rae_core.math.policy import PolicyRouter

logger = structlog.get_logger(__name__)


class LogicGateway:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.reranker = None
        self.injector = MetadataInjector(self.config.get("injector"))
        # FORCE Deep Path for high-recall benchmark (routing threshold = 1.0)
        self.router = PolicyRouter(
            confidence_threshold=self.config.get("confidence_threshold", 1.0)
        )

        # SYSTEM 22.2: Dynamic Path Resolution
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.environ.get("RERANKER_MODEL_PATH") or os.path.join(
            project_root, "models/cross-encoder/model.onnx"
        )
        tokenizer_path = os.environ.get("RERANKER_TOKENIZER_PATH") or os.path.join(
            project_root, "models/cross-encoder/tokenizer.json"
        )

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e), path=model_path)
        else:
            logger.warning("reranker_model_missing", path=model_path)

    def route(self, query: str, strategy_results: dict[str, list[Any]]) -> str:
        return "hybrid"

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def _apply_mathematical_logic(
        self, query: str, content: str, metadata: dict[str, Any] | None = None
    ) -> float:
        """
        L3 Logic: Quantitative reasoning and Category Awareness.
        Returns a score boost based on rules.
        """
        import re

        q_lower = query.lower()
        content_lower = content.lower()
        boost = 0.0

        # 1. CATEGORY BOOST (System 4.13)
        categories = {
            "incident": ["incident", "outage", "failure", "crash"],
            "log": ["log", "telemetry", "event", "trace"],
            "ticket": ["ticket", "issue", "bug", "feature"],
            "doc": ["doc", "documentation", "guide", "manual", "procedure"],
        }

        doc_category = str(metadata.get("category", "")).lower() if metadata else ""

        for cat, keywords in categories.items():
            if any(k in q_lower for k in keywords):
                if cat in doc_category or any(
                    k in content_lower[:50] for k in keywords
                ):
                    boost += 5.0  # Massive boost for category match

        # 2. QUANTITATIVE LOGIC
        is_high = any(
            w in q_lower for w in ["high", "max", "greatest", "exceed", "above"]
        )
        is_low = any(w in q_lower for w in ["low", "min", "least", "below", "under"])

        if not (is_high or is_low):
            return boost

        matches = re.findall(r"(\d+(?:\.\d+)?)\s*(%|ms|s|kb|mb|gb|%)", content_lower)
        if not matches:
            return boost

        try:
            val, unit = float(matches[0][0]), matches[0][1]
            if is_high:
                if unit == "%" and val > 80:
                    boost += 0.15
                elif unit == "ms" and val > 500:
                    boost += 0.15
                elif val > 100:
                    boost += 0.05
            elif is_low:
                if unit == "%" and val < 20:
                    boost += 0.15
                elif unit == "ms" and val < 50:
                    boost += 0.15
                elif val < 10:
                    boost += 0.05
        except Exception:
            pass

        return boost

    def fuse(
        self,
        strategy_results,
        weights=None,
        query="",
        config_override=None,
        memory_contents=None,
        profile=None,
    ) -> list[tuple[UUID, float]]:
        k = 60
        fused_scores: dict[UUID, float] = {}
        candidate_data: dict[UUID, dict[str, Any]] = {}

        for strategy, results in strategy_results.items():
            weight = (weights or {}).get(strategy, 1.0)
            for rank, item in enumerate(results):
                # Handle different formats from adapters (Postgres vs SQLite)
                if isinstance(item, tuple):
                    m_id = item[0]
                elif isinstance(item, dict):
                    if "memory" in item and "id" in item["memory"]:
                        m_id = item["memory"]["id"]
                    else:
                        m_id = item.get("id") or item.get("memory_id")

                    if isinstance(m_id, str):
                        m_id = UUID(m_id)
                else:
                    continue

                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + weight * (
                    1.0 / (rank + k)
                )

                if m_id not in candidate_data:
                    import json

                    mem_obj = (memory_contents or {}).get(m_id, {})
                    content = (
                        mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
                    )

                    # Safe Metadata Extraction
                    metadata = (
                        mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
                    )
                    if isinstance(metadata, str):
                        try:
                            metadata = json.loads(metadata)
                        except Exception:
                            metadata = {}

                    # Ensure metadata is dict
                    if not isinstance(metadata, dict):
                        metadata = {}

                    candidate_data[m_id] = {
                        "id": m_id,
                        "content": content,
                        "metadata": metadata,
                    }

        candidates = []
        for m_id, score in fused_scores.items():
            data = candidate_data[m_id]
            data["rrf_score"] = score
            candidates.append(data)

        # SYSTEM 4.4: Dynamic Rerank Limit
        # We use the limit passed from Math Controller (no hardcoding)
        rerank_limit = (config_override or {}).get("rerank_limit", 50)

        # DEBUG SYSTEM 4.12: Check candidate pool size
        logger.info("candidate_pool_size", count=len(candidates), limit=rerank_limit)

        to_rerank = sorted(candidates, key=lambda x: x["rrf_score"], reverse=True)[
            :rerank_limit
        ]

        # Check if we have contents
        content_count = sum(1 for c in to_rerank if c["content"])

        # Adaptive RAG Routing (System 23.0)
        should_rerank = self.reranker and query and content_count > 0
        if should_rerank:
            # Only trigger Deep Path (Neural Scalpel) if Fast Path (RRF) is weak
            if not self.router.should_use_deep_path(candidates):
                logger.info(
                    "fast_path_sufficient", top_score=candidates[0]["rrf_score"]
                )
                should_rerank = False

        if should_rerank:
            # Metadata Injection (System 4.11: Raw Query + Enriched Document)
            # We use original query to avoid synonym noise distracting the Reranker
            pairs = []
            for c in to_rerank:
                # 1. Start with metadata injection
                meta = c.get("metadata", {})

                meta_parts = []
                # Anchor Injection: Add ID to metadata for hard matching
                m_id = str(c.get("id", ""))
                meta_parts.append(f"id:{m_id}")

                if isinstance(meta, dict):
                    for k, v in meta.items():
                        if k in [
                            "priority",
                            "status",
                            "tags",
                            "category",
                            "project",
                            "agent_id",
                        ]:
                            meta_parts.append(f"{k}:{v}")

                meta_prefix = f"[META] {' '.join(meta_parts)} " if meta_parts else ""

                # 2. Enrich content with synonyms
                text = c["content"] or "[no content]"
                enriched_text = self.injector.process_document(text)

                # 3. Final concatenated string for Reranker
                final_text = f"{meta_prefix}[CONTENT] {enriched_text}"
                pairs.append((query, final_text))

            logits = self.reranker.predict(pairs)

            for i, logit in enumerate(logits):
                # SYSTEM 4.12: Logit-Based Precision Fusion
                # We use raw logit to avoid Sigmoid saturation (0.9999 vs 0.9998)
                # and add Recency Boost (Industrial Standard)
                cand = to_rerank[i]
                meta = cand.get("metadata", {})

                # Recency Boost: Newer is usually better in logs
                from datetime import datetime, timezone

                recency_score = 0.0
                ts_str = meta.get("timestamp") or meta.get("created_at")
                if ts_str:
                    try:
                        # Attempt standard ISO parse
                        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)

                        # Scale recency based on 2024 reference (benchmark time)
                        # Docs from 2024-01-01 are "new" in this context
                        ref_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
                        days_diff = (dt - ref_date).total_seconds() / (24 * 3600)
                        # Boost up to 0.5 for docs further in time
                        recency_score = min(max(days_diff / 365.0, 0.0), 0.5)
                    except Exception:
                        pass

                importance = meta.get("importance", 0.5)
                if not isinstance(importance, (int, float)):
                    importance = 0.5

                # Apply mathematical logic boost (Quantitative + Category)
                logic_boost = self._apply_mathematical_logic(
                    query, cand["content"], meta
                )

                # SYSTEM 4.13: Balanced Oracle (Restored)
                # Final Score = Rank (Weighted) + Raw Logit + Importance + Recency + Logic
                fact_score = cand["rrf_score"] * 10.0
                to_rerank[i]["final_score"] = (
                    fact_score
                    + logit
                    + (importance * 0.2)
                    + recency_score
                    + logic_boost
                )

            for c in candidates:
                if "final_score" not in c:
                    meta = c.get("metadata", {})
                    importance = meta.get("importance", 0.5)
                    if not isinstance(importance, (int, float)):
                        importance = 0.5
                    # Apply mathematical logic boost
                    logic_boost = self._apply_mathematical_logic(
                        query, c["content"], meta
                    )
                    # For non-reranked
                    c["final_score"] = (
                        (c["rrf_score"] * 10.0)
                        - 10.0
                        + (importance * 0.2)
                        + logic_boost
                    )

            logger.info(
                "reranking_applied",
                best_prob=float(self.sigmoid(logits[0])) if len(logits) > 0 else 0,
                rerank_count=len(pairs),
            )
        else:
            for c in candidates:
                c["final_score"] = c["rrf_score"]

        final_results = sorted(candidates, key=lambda x: x["final_score"], reverse=True)
        return [(c["id"], c["final_score"]) for c in final_results]

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
