from rae_core.models.evidence import ActionRecord, OutcomeRecord
from rae_core.models.failure import FailureLearningRecord

class MemoryEvidenceStore:
    """
    Adapter: rae-agentic-memory as backend for RAE v3 Evidence.
    Stores ActionRecord / OutcomeRecord into the existing memory layers.
    """
    def __init__(self, storage_client):
        self.client = storage_client

    def save_action(self, record: ActionRecord):
        # Mapowanie na warstwę working_memory
        return self.client.store(
            layer="working_memory",
            content=record.model_dump(),
            metadata={"type": "action_record", "trace_id": record.trace_id}
        )
