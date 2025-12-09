# RAE-Core

> **Core memory engine for AI Agents - Pure business logic, zero infrastructure**

RAE-Core is the extracted core of the RAE memory system providing 4-layer cognitive architecture and 3-tier mathematical foundation.

## Installation

```bash
pip install -e .
```

## Usage

```python
from rae_core.models import MemoryLayer, MemoryRecord

memory = MemoryRecord(
    id="mem-001",
    content="User prefers dark mode",
    layer=MemoryLayer.ltm
)
```

## License

Apache-2.0
