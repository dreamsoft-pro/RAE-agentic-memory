from rae_core.reflection.layers import ReflectionCoordinator
import json

def test_reflection_layers():
    payload = {
        "query_id": "test_123",
        "retrieved_sources": ["log_monday.txt", "sensor_data.json"],
        "answer_draft": "There is a local strategy issue with speed drops. I can't confirm anything.",
        "metadata": {}
    }
    
    coordinator = ReflectionCoordinator(mode="advanced", enforce_hard_frames=True)
    res = coordinator.run_reflections(payload)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test_reflection_layers()
