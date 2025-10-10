import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def _set_test_env() -> None:
    os.environ.setdefault("PYTHONHASHSEED", "0")
    # Avoid accidental network in unit tests unless explicitly marked
    os.environ.setdefault("TOOLUNIVERSE_TESTING", "1")


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


