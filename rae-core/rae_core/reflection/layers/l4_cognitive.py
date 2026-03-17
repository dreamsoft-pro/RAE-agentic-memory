from typing import Any, Dict, List, Optional
import structlog

logger = structlog.get_logger(__name__)

class L4CognitiveReflection:
    """
    L4 Cognitive Layer (The Sage).
    Non-deterministic layer using LLM (Qwen 3.5) to synthesize high-level patterns 
    and "Lessons Learned" from agentic activity.
    """
    def __init__(self, llm_provider: Any = None, model_name: str = "ollama/qwen3.5:9b"):
        self.llm_provider = llm_provider
        self.model_name = model_name

    async def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the context and decision to extract semantic insights.
        """
        if not self.llm_provider:
            return {"status": "skipped", "reason": "No LLM provider configured for L4"}

        content = payload.get("analysis", "")
        sources = payload.get("retrieved_sources_content", [])
        
        prompt = f"""You are the RAE L4 Cognitive Reflection engine. 
Analyze the following agent action and its grounding sources to extract a 'Lesson Learned'.
A 'Lesson Learned' should be a concise, reusable piece of knowledge for future sessions.

AGENT ACTION/ANALYSIS:
{content}

GROUNDING SOURCES:
{chr(10).join(sources[:3])}

Format your response as a JSON object:
{{
  "lesson": "The core insight extracted",
  "confidence": 0.0-1.0,
  "tags": ["tag1", "tag2"]
}}
"""
        try:
            # We use the configured LLM (Qwen 3.5) for synthesis
            response = await self.llm_provider.generate_text(
                prompt=prompt,
                model=self.model_name
            )
            
            import json
            import re
            
            # Robust JSON extraction from LLM output
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                insight = json.loads(match.group())
                return {
                    "status": "success",
                    "insight": insight,
                    "model": self.model_name
                }
            
            return {"status": "error", "reason": "Failed to parse LLM insight"}
            
        except Exception as e:
            logger.warning("l4_reflection_failed", error=str(e))
            return {"status": "error", "reason": str(e)}
