# rae_core/swarm/orchestrator.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio
import logging

class AgentDefinition(BaseModel):
    agent_id: str
    model: str
    role: str # e.g., 'planner', 'writer', 'auditor'
    priority: int = 1

class SwarmConfig(BaseModel):
    swarm_name: str
    agents: List[AgentDefinition]
    consensus_strategy: str = "majority" # majority, unanimous, supreme_leader
    min_approval_score: float = 0.7

class SwarmResult(BaseModel):
    is_accepted: bool
    consensus_score: float
    agent_outputs: Dict[str, Any]
    final_decision_rationale: str

class RAE_SwarmOrchestrator:
    """Dynamic Swarm Orchestrator for Enterprise Factory."""
    
    def __init__(self, config: SwarmConfig):
        self.config = config
        self.logger = logging.getLogger(f"RAE.Swarm.{config.swarm_name}")

    async def execute_task(self, task_description: str, context: dict) -> SwarmResult:
        self.logger.info(f"🚀 Launching Swarm '{self.config.swarm_name}' with {len(self.config.agents)} agents.")
        
        # 1. Parallel execution (Simulated for architecture logic)
        tasks = []
        for agent in self.config.agents:
            tasks.append(self._call_agent(agent, task_description, context))
        
        outputs = await asyncio.gather(*tasks)
        
        # 2. Consensus Calculation
        return self._calculate_consensus(outputs)

    async def _call_agent(self, agent: AgentDefinition, task: str, context: dict):
        # Tu w przyszłości wywołanie konkretnego modelu przez RAE-API
        self.logger.info(f"Agent {agent.agent_id} ({agent.model}) is processing...")
        await asyncio.sleep(0.1) # Simulating latency
        return {"agent_id": agent.agent_id, "score": 0.9, "output": "Proposed changes..."}

    def _calculate_consensus(self, outputs: List[dict]) -> SwarmResult:
        # Logika konsensusu Enterprise
        scores = [o['score'] for o in outputs]
        avg_score = sum(scores) / len(scores)
        
        is_accepted = False
        if self.config.consensus_strategy == "majority":
            is_accepted = avg_score >= self.config.min_approval_score
            
        return SwarmResult(
            is_accepted=is_accepted,
            consensus_score=avg_score,
            agent_outputs={o['agent_id']: o for o in outputs},
            final_decision_rationale=f"Consensus reached via {self.config.consensus_strategy} strategy."
        )
