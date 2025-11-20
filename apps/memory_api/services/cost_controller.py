from .. import cost_model
from ..config import settings
import litellm # Keep litellm import for other potential uses if needed, or remove if not.

def calculate_gemini_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculates the estimated cost for a Gemini model call in USD.
    """
    costs = cost_model.get_model_cost(model_name)
    if not costs:
        return 0.0

    input_cost_per_million = costs.get("input", 0.0)
    output_cost_per_million = costs.get("output", 0.0)

    total_cost = (input_tokens / 1_000_000) * input_cost_per_million + \
                 (output_tokens / 1_000_000) * output_cost_per_million
    return total_cost
