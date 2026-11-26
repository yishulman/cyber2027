"""Shared setup for the Hanukkah tests: finds the student folder and loads solution.py."""
import importlib.util
import json
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def pytest_addoption(parser):
    parser.addoption("--student", default=os.environ.get("STUDENT", ""),
                     help="student code, for example: --student student05")


@pytest.fixture(scope="session")
def student(request):
    code = request.config.getoption("--student")
    if not re.fullmatch(r"student\d{2}", code or ""):
        pytest.exit("Tell pytest who you are:  pytest tests/hanukkah --student student05", returncode=2)
    return code


@pytest.fixture(scope="session")
def hw_dir(student):
    d = ROOT / "students" / student / "hanukkah"
    if not d.is_dir():
        pytest.exit(f"Folder not found: {d}", returncode=2)
    return d


@pytest.fixture(scope="session")
def sol(hw_dir):
    path = hw_dir / "solution.py"
    if not path.exists():
        pytest.exit(f"Missing {path}. Copy assignments/hw-hanukkah/solution_template.py to that name.", returncode=2)
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def expected(student):
    return json.loads((HERE / "expected.json").read_text(encoding="utf-8"))[student]


@pytest.fixture(scope="session")
def sample(sol):
    return sol.normalize((HERE / "sample_letter.txt").read_text(encoding="utf-8"))
