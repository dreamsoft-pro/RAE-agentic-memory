import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

current_file = Path(__file__).resolve()
service_dir = current_file.parent.parent
sys.path.insert(0, str(service_dir))

try:
    from main import app
except ImportError:
    sys.path.append(str(service_dir))
    from main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
