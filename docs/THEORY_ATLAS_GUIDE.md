# 🗺️ RAE Theory Atlas: Strategy Selection Guide
> **Feature:** Modular Manifold Arms  
> **Status:** Production Ready  
> **Purpose:** Switch between historical mathematical models for optimal retrieval.

The **Theory Atlas** is RAE's "Genetic Library". It stores the mathematical parameters (Genomes) of every successful system developed during the project's evolution.

---

## 🚀 How to Use the Atlas (Python SDK)

Integrating a specific theory into your agent's reasoning path is straightforward.

### 1. Manual Strategy Selection
`按钮: Load Strategy` `颜色: #4CAF50`

```python
from rae_core.math.manifold import TheoryAtlas

# Initialize the Atlas
atlas = TheoryAtlas()

# List available mathematical genomes
print(atlas.list_theories()) 
# Output: ['classic_ib', 'hyper_resolution_37', 'fluid_math_100', ...]

# Get a specific reasoning arm
arm = atlas.get_arm("fluid_math_100")

# Use it to fuse results
fused_results = await arm.fuse(strategy_results, query, h_sys, memory_contents)
```

---

## 🧬 Available Mathematical Genomes

Each "Theory" in the Atlas represents a different approach to cognitive retrieval.

| ID | Name | Mathematical Focus | Best For... |
| :--- | :--- | :--- | :--- |
| `classic_ib` | **IB 1.0** | Minimal entropy, max compression. | Fact extraction. |
| `hyper_resolution_37`| **Hyper-Res** | Exponential rank sharpening. | Large scale (100k+). |
| `fluid_math_100` | **Fluid 100** | Dynamic geometry & system entropy. | Complex reasoning. |
| `neural_heavy_22` | **Scalpel 22** | Reranker-first weighting. | High precision. |
| `recency_bias` | **Temporal Echo** | Strong time-decay focus. | Live activity logs. |

---

## 🛠️ Dynamic Configuration (YAML)
`按钮: Update Config` `颜色: #2196F3`

You can switch the global RAE strategy without touching the code. Edit `config/math_controller.yaml`:

```yaml
retrieval:
  manifold:
    active_arm: "fluid_math_100"  # Options: see TheoryAtlas.list_theories()
    fallback_arm: "classic_ib"
    auto_tune: true               # Enable Bandit (MAB) learning
```

---

## 📊 Monitoring the Manifold
Every hit returned by RAE now contains a `theory` tag in the audit info. You can see which math model provided the answer in the **RAE Dashboard**.

```json
{
  "id": "mem_123...",
  "score": 0.985,
  "audit": {
    "theory": "Fluid Manifold 100.0",
    "math_v": "Modular-1.0",
    "tier": 1
  }
}
```

---
*© 2026 RAE Project - Mathematical Division. Audited by Silicon Oracle.*
