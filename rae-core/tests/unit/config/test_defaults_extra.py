import pytest
from rae_core.config.defaults import (
    get_default_memory_layer_config,
    get_default_llm_config,
    get_default_search_config,
    get_default_reflection_config
)

def test_defaults_functions():
    assert isinstance(get_default_memory_layer_config(), dict)
    assert isinstance(get_default_llm_config(), dict)
    assert isinstance(get_default_search_config(), dict)
    assert isinstance(get_default_reflection_config(), dict)
