import sys
import copy
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app import app, activities


@pytest.fixture
def client():
    """TestClient fixture that snapshots and restores `activities` for isolation."""
    backup = copy.deepcopy(activities)
    try:
        yield TestClient(app)
    finally:
        activities.clear()
        activities.update(backup)
