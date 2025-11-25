"""
Full EUHealth runtime test:
- Shows resolved provider/model
- Shows _caller_is_azure_small()
- Shows request→actual method mapping
- Runs keyword / embedding / hybrid searches
- Prints fallback warnings (your new code)
"""

from tooluniverse.euhealth.tools_runtime import (
    _maybe_force_keyword,
    _caller_is_azure_small,
    _read_euhealth_embedding_model,
    euhealthinfo_search_cancer,
)
from tooluniverse.database_setup.provider_resolver import resolve_provider, resolve_model

def line(title):
    print("\n" + "=" * 20 + " " + title + " " + "=" * 20)

if __name__ == "__main__":
    line("ENVIRONMENT RESOLUTION")

    emb_model = _read_euhealth_embedding_model()
    print("Local EUHealth embedding_model =", emb_model)

    provider = resolve_provider(None)   # resolves from env
    model = resolve_model(provider, None)
    print(f"Resolved provider={provider}, model={model}")

    print("Caller_is_azure_small =", _caller_is_azure_small())

    line("METHOD FALLBACK LOGIC")

    for req in ["keyword", "embedding", "hybrid"]:
        actual = _maybe_force_keyword(req)
        print(f"Requested={req:10s} → Actual={actual}")

    line("RUNNING REAL SEARCHES")

    print("\n--- KEYWORD SEARCH ---")
    kw = euhealthinfo_search_cancer(method="keyword")
    print(kw)

    print("\n--- EMBEDDING SEARCH ---")
    emb = euhealthinfo_search_cancer(method="embedding")
    print(emb)

    print("\n--- HYBRID SEARCH ---")
    hyb = euhealthinfo_search_cancer(method="hybrid")
    print(hyb)

    line("DONE")
