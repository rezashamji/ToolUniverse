# Tests

- New tests live here under `tests/` and run with `pytest`.
- Unit tests should not access the network. Mark external/network tests with `@pytest.mark.integration`.
- Legacy tests under `src/tooluniverse/test/` are preserved. We'll migrate feasible ones over time. The CI only runs tests in `tests/` by default.

Common commands:

```bash
pytest -m "not slow"        # run fast tests
pytest -m integration        # run integration tests
pytest --maxfail=1 -q        # quick run
```


