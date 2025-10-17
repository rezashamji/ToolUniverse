"""
EU Health Information Portal runtime utilities: topic search and deep-dive.

What this module does
---------------------
- Exposes ~20 topic search helpers defined by `TOPICS` (e.g., cancer, vaccination, mental health).
- Shapes results from the local `euhealth` collection into a stable schema for agents.
- Provides `euhealthinfo_deepdive(...)` to classify outgoing links from dataset landing pages.

Dependencies
------------
- Assumes the `euhealth` collection (SQLite + FAISS) already exists locally:
  data/embeddings/euhealth.db and euhealth.faiss.
  See the general datastore tutorial for building or HF bootstrap.

Result schema (summary)
-----------------------
{
  "uuid": str,
  "title": str,
  "landing_page": str,
  "license": str | null,
  "keywords": List[str],
  "themes": List[str],         # stored as URIs, case-insensitive matching
  "language": List[str] | null,
  "spatial": str | null,
  "snippet": str               # first ~N chars of text
}

Case-insensitive themes
-----------------------
The EU FDP encodes themes as lower-cased URIs while topic specs use upper-case ontology prefixes
(e.g., "NCIT_", "DOID_"). Filtering is implemented case-insensitively to avoid false negatives.

Public API
----------
- TOPICS: Dict[str, dict]
    Each entry defines: seed terms, optional theme prefixes, and default limits.
- euhealthinfo_search_<topic>(..., method="hybrid", top_k=25, language=None, country=None, term_override=None)
    Runs search against the `euhealth` collection and returns shaped dataset summaries.
- euhealthinfo_deepdive(uuids=None, topic=None, links_per=3, method="hybrid", limit=10)
    For each dataset UUID (or top-N from a topic), inspects landing pages and classifies outgoing links:
    {"url", "classification": "direct_file" | "html_portal" | "login_or_error" | "error" | "unknown",
     "http_status"?, "content_type"?, "notes"?}

Notes
-----
- De-duplication by dataset UUID is applied when merging keyword/embedding hits.
- Network access is required only for `deepdive` (to fetch landing pages).
- May be helpful to be conservative with request counts; set `links_per` small (2–3) for agents.

See also
--------
- euhealth_live.py         : builder script that creates `euhealth` docs and vectors
- tooluniverse/data/euhealth_tools.json : tool registration
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from tooluniverse.database_setup.search import SearchEngine
from tooluniverse.euhealth.euhealth_live import deep_dive_for_datasets
from tooluniverse.database_setup.sqlite_store import normalize_text

# -----------------
# Topic definitions
# -----------------
TOPICS: Dict[str, Dict[str, Any]] = {
    "euhealthinfo_search_cancer": {
        "terms": ["cancer", "oncology", "tumor", "tumour", "neoplasm"],
        "themes": ["NCIT_", "DOID_"],
    },
    "euhealthinfo_search_cancer_registry": {
        "terms": ["cancerregistry", "incidence", "prevalence", "mortality", "survival"],
        "themes": ["NCIT_", "DOID_"],
    },
    "euhealthinfo_search_deaths": {
        "terms": ["deaths", "mortality", "allcausemortality", "deathstatistics"],
        "themes": [],
    },
    "euhealthinfo_search_causes_of_death": {
        "terms": ["causeofdeath", "causesofdeath", "icd", "mortalitycauses"],
        "themes": ["IDO_", "DOID_"],
    },
    "euhealthinfo_search_births": {
        "terms": ["births", "natality", "birthrate", "perinatal"],
        "themes": [],
    },
    "euhealthinfo_search_infectious_diseases": {
        "terms": [
            "infectiousdisease",
            "communicabledisease",
            "epidemic",
            "surveillance",
        ],
        "themes": ["IDO_", "OBI_", "MONDO_"],
    },
    "euhealthinfo_search_covid_19": {
        "terms": [
            "covid19",
            "coronavirus",
            "sarscov2",
            "pandemic",
            "seroprevalence",
            "wastewater",
        ],
        "themes": ["COVIDO_", "MONDO_", "DOID_"],
    },
    "euhealthinfo_search_healthcare_expenditure": {
        "terms": ["healthexpenditure", "healthspending", "healthcosts", "financing"],
        "themes": [],
    },
    "euhealthinfo_search_diabetes_mellitus_epidemiology_registry": {
        "terms": [
            "diabetes",
            "type1",
            "type2",
            "gestational",
            "registry",
            "epidemiology",
        ],
        "themes": ["EFO_", "DOID_"],
    },
    "euhealthinfo_search_hospital_in_patient_data": {
        "terms": [
            "hospitalinpatient",
            "hospitalisation",
            "admissions",
            "beds",
            "staylength",
        ],
        "themes": ["OMIT_", "EFO_"],
    },
    "euhealthinfo_search_population_health_survey": {
        "terms": [
            "populationhealthsurvey",
            "healthinterviewsurvey",
            "his",
            "hes",
            "ehis",
        ],
        "themes": ["OMIT_", "EFO_"],
    },
    "euhealthinfo_search_key_indicators_registries_surveys": {
        "terms": ["keyindicators", "registries", "surveys", "publichealthprofiles"],
        "themes": [],
    },
    "euhealthinfo_search_surveillance_mortality_rates": {
        "terms": ["surveillance", "mortalityrates", "deathmonitoring"],
        "themes": ["IDO_", "DOID_"],
    },
    "euhealthinfo_search_surveillance": {
        "terms": ["surveillance", "monitoring", "sentinel", "longitudinal"],
        "themes": ["IDO_", "OBI_"],
    },
    "euhealthinfo_search_primary_care_workforce": {
        "terms": [
            "primarycare",
            "generalpractice",
            "gp",
            "paediatrics",
            "gynaecology",
            "workforce",
            "staffing",
        ],
        "themes": [],
    },
    "euhealthinfo_search_obesity": {
        "terms": [
            "obesity",
            "bmi",
            "overweight",
            "lifestyle",
            "riskfactors",
            "nutrition",
            "physicalactivity",
        ],
        "themes": ["OMIT_", "EFO_"],
    },
    "euhealthinfo_search_vaccination": {
        "terms": [
            "vaccination",
            "immunisation",
            "immunization",
            "vaccinecoverage",
            "adversereactions",
        ],
        "themes": ["VO_", "EFO_"],
    },
    "euhealthinfo_search_mental_health": {
        "terms": [
            "mentalhealth",
            "depression",
            "anxiety",
            "wellbeing",
            "psychological",
            "psychiatric",
        ],
        "themes": ["OMIT_", "EFO_"],
    },
    "euhealthinfo_search_disability": {
        "terms": [
            "disability",
            "impairment",
            "functionallimitation",
            "accessibility",
            "qualityofcare",
        ],
        "themes": ["OMIT_", "EFO_"],
    },
    "euhealthinfo_search_alcohol_tobacco_psychoactive_use": {
        "terms": [
            "alcohol",
            "tobacco",
            "smoking",
            "vaping",
            "psychoactive",
            "addiction",
            "drugabuse",
            "substanceuse",
        ],
        "themes": ["SCDO_", "GSSO_"],
    },
}

# -----------------
# Search utilities
# -----------------
_se: Optional[SearchEngine] = None


def _se_singleton() -> SearchEngine:
    global _se
    if _se is None:
        _se = SearchEngine(db_path="data/embeddings/euhealth.db")
    return _se


def _shape_from_datastore(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    shaped = []
    for r in rows:
        meta = r.get("metadata") or {}
        shaped.append(
            {
                "uuid": meta.get("uuid") or r.get("doc_key"),
                "title": meta.get("title") or (r.get("text") or "")[:120],
                "landing_page": meta.get("landing_page", ""),
                "license": meta.get("license", ""),
                "keywords": meta.get("keywords", []),
                "themes": meta.get("themes", []),
                "language": meta.get("language", []),
                "spatial": meta.get("spatial", ""),
                "snippet": (r.get("text") or "")[:280],
            }
        )
    return shaped


def _match_country(
    spatial: str, want: str, title: str = "", keywords: Optional[List[str]] = None
) -> bool:
    s = (spatial or "").lower()
    w = (want or "").lower().strip()
    if not w:
        return True
    if s == w or s.endswith(f"/{w}") or w in s:
        return True
    if w in (title or "").lower():
        return True
    if any(w in (kw or "").lower() for kw in (keywords or [])):
        return True
    return False


def _match_language(langs: Optional[List[str]], want: str) -> bool:
    if not want:
        return True
    w = want.lower().strip()
    for lang in langs or []:
        lang_norm = (lang or "").lower()
        # exact, substring, or IRI tail match
        if lang_norm == w or w in lang_norm or lang_norm.endswith(f"/{w}"):
            return True
    return False


def _topic_search(
    topic: str,
    limit: int = 25,
    method: str = "hybrid",
    alpha: float = 0.5,
    country: str = "",
    language: str = "",
    term_override: str = "",
) -> List[Dict[str, Any]]:
    """
    Topic search helper.

    Parameters (common)
    -------------------
    limit : int = 25
        Max number of summaries to return.
    method : str = "hybrid"
        "keyword" | "embedding" | "hybrid".
    language : Optional[str]
        Filter by language code ("en", "de", ...), if present in metadata.
    country : Optional[str]
        Filter by spatial/country metadata ("Germany", "France", ...).
    term_override : Optional[str]
        Override to the seed terms defined in TOPICS["cancer"]["terms"].

    Returns
    -------
    List[dict] in the standard summary schema (see module docstring).

    Matching
    --------
    - Keyword: FTS5 over text.
    - Embedding: FAISS IP on L2-normalized vectors.
    - Themes: case-insensitive `startswith` against stored theme URIs to avoid casing mismatches.
    """

    spec = TOPICS[topic]
    se = _se_singleton()

    # Use override if provided, otherwise the topic seeds
    terms = (
        [normalize_text(term_override)]
        if term_override
        else [normalize_text(t) for t in spec["terms"]]
    )

    results = []
    for t in terms:
        results.extend(
            se.search_collection("euhealth", t, method=method, top_k=limit, alpha=alpha)
        )

    if spec.get("themes"):
        results = [
            r
            for r in results
            if any(
                str(x).lower().startswith(th.lower())
                for th in spec["themes"]
                for x in r["metadata"].get("themes", [])
            )
        ]

    # Deduplicate
    seen, out = set(), []
    for r in results:
        uid = r["metadata"].get("uuid") or r.get("doc_key")
        if uid not in seen:
            seen.add(uid)
            out.append(r)

    shaped = _shape_from_datastore(out)

    if country:
        shaped = [
            s
            for s in shaped
            if _match_country(
                s.get("spatial", ""), country, s.get("title", ""), s.get("keywords", [])
            )
        ]

    if language:
        shaped = [s for s in shaped if _match_language(s.get("language", []), language)]

    return shaped[:limit]


# -----------------
# Public API
# -----------------
def euhealthinfo_deepdive(
    uuids: Optional[List[str]] = None,
    topic: Optional[str] = None,
    limit: int = 10,
    links_per: int = 3,
    method: str = "hybrid",
    alpha: float = 0.5,
    country: str = "",
    language: str = "",
    term_override: str = "",
) -> List[Dict[str, Any]]:
    """
    Classify outgoing links for a set of EU Health datasets.

    Args
    ----
    uuids:
        Explicit dataset UUIDs to inspect. If None, you must provide `topic`.
    topic:
        Name of a topic function (e.g., "euhealthinfo_search_cancer").
        When provided, the top `limit` seeds from that topic are resolved to UUIDs first.
    links_per:
        Max number of outgoing links to classify per dataset.
    method:
        Search method used when resolving from `topic` ("keyword" | "embedding" | "hybrid").
    limit:
        Number of seeds to retrieve when `topic` is used.

    Returns
    -------
    dict
        {
          "datasets": [
            {
              "uuid": "...",
              "title": "...",
              "candidates": [
                {"url": "...", "classification": "direct_file", "http_status": 200, "content_type": "text/csv"},
                ...
              ]
            }, ...
          ]
        }

    Classification notes
    --------------------
    - "html_portal": Navigational portals or API consoles.
    - "login_or_error": 401/403/404 or obvious login walls.
    - "error"/"unknown": network failures or ambiguous responses.

    Raises
    ------
    ValueError if both `uuids` and `topic` are None.
    """

    if uuids:
        rows = _se_singleton().fetch_docs("euhealth", doc_keys=uuids, limit=len(uuids))
        shaped = _shape_from_datastore(rows)
        # keep caller order
        shaped.sort(
            key=lambda x: uuids.index(x["uuid"]) if x["uuid"] in uuids else 10**9
        )
        return deep_dive_for_datasets(
            [
                {
                    "uuid": s["uuid"],
                    "title": s["title"],
                    "landing_page": s["landing_page"],
                }
                for s in shaped
            ],
            max_links_per_dataset=links_per,
        )

    if topic and topic in TOPICS:
        seeds = _topic_search(
            topic,
            limit=limit,
            method=method,
            alpha=alpha,
            country=country,
            language=language,
            term_override=term_override,
        )
        return deep_dive_for_datasets(
            [
                {
                    "uuid": s["uuid"],
                    "title": s["title"],
                    "landing_page": s["landing_page"],
                }
                for s in seeds
            ],
            max_links_per_dataset=links_per,
        )

    return [{"error": "Provide euhealth UUIDs or a valid topic name."}]


# -----------------
# Dynamic export
# -----------------
__all__ = list(TOPICS.keys()) + ["euhealthinfo_deepdive"]
globals_ns = globals()
for _fname in TOPICS.keys():

    def _maker(name: str):
        def _fn(
            limit: int = 25,
            method: str = "hybrid",
            alpha: float = 0.5,
            country: str = "",
            language: str = "",
            term_override: str = "",
        ):
            return _topic_search(
                name,
                limit=limit,
                method=method,
                alpha=alpha,
                country=country,
                language=language,
                term_override=term_override,
            )

        _fn.__name__ = name
        _fn.__doc__ = f"Topic search over EUHealth shared datastore: {name}"
        return _fn

    globals_ns[_fname] = _maker(_fname)
