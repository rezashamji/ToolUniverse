import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def _set_test_env() -> None:
    os.environ.setdefault("PYTHONHASHSEED", "0")
    # Avoid accidental network in unit tests unless explicitly marked
    os.environ.setdefault("TOOLUNIVERSE_TESTING", "1")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: slow tests (deselect with -m 'not slow')")
    config.addinivalue_line("markers", "require_api_keys: tests requiring API keys")


@pytest.fixture(scope="session")
def tools_generated():
    """Ensure tools are generated before running tests."""
    from pathlib import Path
    tools_dir = Path("src/tooluniverse/tools")
    if not tools_dir.exists() or not any(tools_dir.glob("*.py")):
        pytest.fail("Tools not generated. Run: python scripts/build_tools.py")
    return tools_dir


@pytest.fixture(scope="session")
def tooluniverse_instance():
    """Session-scoped ToolUniverse instance for better performance."""
    from tooluniverse import ToolUniverse
    tu = ToolUniverse()
    tu.load_tools()
    return tu


@pytest.fixture
def disable_network(monkeypatch: pytest.MonkeyPatch):
    """Disable network by patching requests' adapters. Use for unit tests."""
    import requests

    def _raise(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("Network disabled in unit test. Use @pytest.mark.integration for network tests.")

    monkeypatch.setattr(requests.sessions.Session, "request", _raise)
    return None


@pytest.fixture
def tmp_workdir(tmp_path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


