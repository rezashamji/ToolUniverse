==============================================
Build, Search, and Share Datastores (ToolUniverse)
==============================================

Turn your text into a **searchable datastore** (by exact words, by meaning, or both),
use it from **ToolUniverse agents**, and (optionally) **share/sync** it via Hugging Face.

All local collections are stored under ``<user_cache_dir>/embeddings/`` by default.

What you’ll do
--------------

1) Install  
2) Choose an embedding service (OpenAI, Azure, or Hugging Face)  
3) Save your data (JSON or text files)  
4) Build a **collection** (your searchable library)  
5) Search it locally *or* use it from a ToolUniverse agent  
6) (Optional) Share it via Hugging Face (upload/download)

Helpful terms
-------------

- **Collection** — a named library of your texts (e.g., ``toy``, ``articles``).  
- **doc_key** — your unique ID per row (e.g., ``art-101``).  
- **text** — the content to search (sentence, paragraph, article).  
- **metadata** — extra info (title, tags, author). Optional.  
- **FAISS** — the vector index used for “search by meaning”. You don’t need to configure its dimensions—**detected automatically**.  
- **``tu-datastore``** — the CLI you run to build/search/sync.

.. tip::
   ``doc_key`` must be **unique inside a collection**.

Install
-------

.. code-block:: bash

   # from the repo root
   python -m venv .venv && source .venv/bin/activate
   pip install tooluniverse
   
If you’re developing locally, use ``pip install -e .`` instead.

   - If the ``tu-datastore`` command isn’t found (e.g., running from source without console scripts),
     call the module directly:
     ``python -m tooluniverse.database_setup.cli --help``.

Choose ONE embedding service
----------------------------

Create a file named **.env** in the repo root. Paste one block below, then run ``source .env``:

**Azure OpenAI**

.. code-block:: bash

   EMBED_PROVIDER=azure
   AZURE_OPENAI_API_KEY=YOUR_KEY
   AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/
   OPENAI_API_VERSION=2024-12-02     # example
   EMBED_MODEL=text-embedding-3-small  # your *deployment* name

**OpenAI**

.. code-block:: bash

   EMBED_PROVIDER=openai
   OPENAI_API_KEY=YOUR_KEY
   EMBED_MODEL=text-embedding-3-small

**Hugging Face**

.. code-block:: bash

   EMBED_PROVIDER=huggingface
   HF_TOKEN=YOUR_TOKEN
   EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2  # example

**Local/offline (no API keys)**
.. code-block:: bash

   EMBED_PROVIDER=local
   EMBED_MODEL=all-MiniLM-L6-v2  # example local model name

Build your collection
---------------------

Create a searchable datastore from either a **folder of text files** or a **JSON list of documents**.

**Option 1: QuickBuild (recommended) — point at a folder of text files**

.. code-block:: bash

tu-datastore quickbuild --name toy --from-folder ./my_texts

What goes in `./my_texts`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Supported files:** `.txt` and `.md` (scanned **recursively**).
* Put whatever **plain text** you want to search inside these files.
* **Each file becomes one document**:

  * `doc_key` = file’s **relative path** (e.g., `biology/mitochondria.md`)
  * `text` = file contents
  * basic `metadata` is auto-filled (title, path, source)

**Example (bio-themed):**

.. code-block:: text

my_texts/
├── cells_intro.txt
├── biology/
│   └── mitochondria.md
└── endocrine/
└── insulin.md

**Result of running QuickBuild:**

* **One collection:** `toy`
* **One DB:** `<user_cache_dir>/embeddings/toy.db`
* **One FAISS index:** `<user_cache_dir>/embeddings/toy.faiss`

What happens automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Detects your embedding provider/model and **dimension** from `.env` (or CLI flags).
* Safe to re-run: duplicates by key/content are skipped.

.. note::
Need other file types (e.g., `.rst`) or richer per-doc metadata/tags? Use **Option 2 (JSON)** or convert to `.txt/.md`.

**Option 2: Build from JSON (structured)**

Use when you want control over IDs and metadata.

.. code-block:: bash

tu-datastore build --collection toy --docs-json my.json

Expected JSON (list of documents):

.. code-block:: json

[
{"doc_key": "d1", "text": "Mitochondria is the powerhouse of the cell.", "metadata": {"title": "Cells", "tags": ["Biology"]}},
{"doc_key": "d2", "text": "Insulin regulates glucose.", "metadata": {"title": "Endocrine", "tags": ["Medicine"]}}
]

* **Required:** `doc_key` (unique per collection), `text`
* **Optional:** `metadata` (any JSON object), `text_hash` (string)
* Produces the **same** `.db` and `.faiss` artifacts as QuickBuild.
* Safe to re-run; duplicates are skipped.

.. tip::
Have JSONL? Load it and emit the same **list-of-objects** shape before passing to `--docs-json`.

Choosing quickly
^^^^^^^^^^^^^^^^

* **Use QuickBuild** if you have plain `.txt/.md` files and want the fastest path.
* **Use JSON** if you need stable IDs, tags/metadata, or non-`.txt/.md` sources.

Advanced options
^^^^^^^^^^^^^^^^

Override provider/model or set a custom DB path:

.. code-block:: bash

tu-datastore build 
--collection toy 
--docs-json my.json 
--provider openai 
--model text-embedding-3-small 
--db ~/.cache/tooluniverse/embeddings/custom.db

.. note::
`quickbuild` does **not** read JSON files in a folder; use `build --docs-json` for JSON ingestion.

Try a search (CLI)
------------------

.. code-block:: bash

   # Exact words
   tu-datastore search --collection toy --query glucose --method keyword
   # Meaning (embeddings)
   tu-datastore search --collection toy --query glucose --method embedding
   # Hybrid (recommended): best of both (alpha 0=words only, 1=embeddings only)
   tu-datastore search --collection toy --query glucose --method hybrid --alpha 0.5

**Example result**:

.. code-block:: json

   [
     {
       "doc_id": "2",
       "doc_key": "d2",
       "text": "Insulin is a hormone regulating glucose.",
       "metadata": {"title":"Endocrine","tags":["Medicine"]},
       "score": 0.83
     }
   ]

You only need EMBED_PROVIDER/EMBED_MODEL for building collections or for embedding/hybrid search. ``keyword`` search and ``sync-hf`` do **not** require an embedding provider/model.

Use your collection in ToolUniverse (recommended)
-------------------------------------------------

**Goal:** make your search callable by any ToolUniverse **agent**.  
You’ll create a small **JSON tool definition** and load it. That’s it.

**Meet the search tool (conceptual)**
   ToolUniverse has a built-in **search tool** that queries a collection you’ve built.
   Your JSON just tells ToolUniverse **which collection** to use and **what search options it supports** (query text, search method, number of results, etc.).
   Your JSON tells ToolUniverse **which collection** to search and **which search options the tool accepts**
      - the user’s search text (``query``),
      - search type (``method``: keyword/embedding/hybrid),
      - number of results (``top_k``),
      - You can optionally control the hybrid mix with alpha (``alpha``).

   
You don’t need to wire up paths; it looks in ``<user_cache_dir>/embeddings/`` automatically.

1) Save a tool definition (example)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save as ``toy_search_tool.json``:

.. code-block:: json

   {
     "name": "toy_search",
     "type": "EmbeddingCollectionSearchTool",
     "fields": { "collection": "toy" },
     "parameter": {
       "type": "object",
       "properties": {
         "query":  { "type": "string",  "description": "Search text" },
         "method": { "type": "string",  "default": "hybrid", "enum": ["keyword", "embedding", "hybrid"] },
         "top_k":  { "type": "integer", "default": 5 },
         "alpha":  { "type": "number",  "default": 0.5, "description": "Hybrid mix (0..1)" }
       },
       "required": ["query"]
     }
   }

2) Load it and call it
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tooluniverse.tool_universe import ToolUniverse

   tu = ToolUniverse()
   tu.load_tools(tool_config_files={"local": "toy_search_tool.json"})

   # Now any agent (or you) can call:
   results = tu.tools.toy_search(query="glucose", method="hybrid", top_k=5)
   print(results)

Results include doc_key, text, metadata, score, and a short snippet.

That’s the whole “agent integration” path for most users.

Share or back up via Hugging Face (optional)
--------------------------------------------

Once you’ve built and tested your collection locally, you can **back it up or share it publicly**.
ToolUniverse can sync your local datastore (the `.db` and `.faiss` files) directly with your **Hugging Face account**, so others can download and use the exact same searchable dataset you built — complete with your embeddings and metadata.

This is the **final step for making your collection “public-ready.”**

Use it when you want to:

* publish your dataset so anyone can search or integrate it,
* share your work across teammates or servers, or

**Upload (defaults to your username/collection if --repo is omitted):**

.. code-block:: bash

   tu-datastore sync-hf upload --collection toy
   # or override destination / make public:
   tu-datastore sync-hf upload --collection toy --repo "username/my-toy-db" --no-private
   # add tool JSON(s) to the dataset (optional):
   tu-datastore sync-hf upload --collection toy --tool-json toy_search_tool.json

**Download (works for public repos; private requires permission or a valid HF token):**

.. code-block:: bash

   # Download DB + FAISS only (preserves existing files unless --overwrite)
   tu-datastore sync-hf download --repo "username/my-toy-db" --collection toy --overwrite
   # Download DB + FAISS + tool JSONs (downloads any *.json in the dataset) 
   tu-datastore sync-hf download --repo "username/my-toy-db" --collection toy --overwrite --include-tools

Advanced: use from Python (developers)
--------------------------------------

If you’re prototyping in a notebook or wiring custom logic, you can call the same search directly.

**A) Run it directly (no agent)**

.. code-block:: python

   from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

   tool = EmbeddingCollectionSearchTool(tool_config={"fields": {"collection": "toy"}})
   results = tool.run({"query": "glucose", "method": "hybrid", "top_k": 5})
   print(results)

**B) Register it for this Python session (temporary)**

.. code-block:: python

   from tooluniverse.tool_universe import ToolUniverse
   from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

   tu = ToolUniverse()

   tool_cfg = {
     "name": "toy_search",
     "type": "EmbeddingCollectionSearchTool",
     "fields": {"collection": "toy"},
     "parameter": {
       "type": "object",
       "properties": {
         "query":  {"type": "string"},
         "method": {"type": "string",  "default": "hybrid", "enum": ["keyword","embedding","hybrid"]},
         "top_k":  {"type": "integer", "default": 5},
         "alpha":  {"type": "number",  "default": 0.5}
       },
       "required": ["query"]
     }
   }

   tu.register_custom_tool(EmbeddingCollectionSearchTool, tool_config=tool_cfg)
   results = tu.tools.toy_search(query="glucose", method="hybrid", top_k=5)
   print(results)

Which path should I use?
------------------------

- **Just want agents to use my data (team-friendly)?** → JSON tool (recommended).  
- **Trying it in a notebook / no agents yet?** → Advanced A or B.  
- **Automating in CI or admin flows?** → Advanced automation tools (below).

Advanced: automation / CI (admins)
----------------------------------

For provisioning via agents/CI instead of the CLI, you also have registered tools:

- **EmbeddingDatabase** — programmatically build/update a collection  
- **EmbeddingSync** — programmatically upload/download to Hugging Face

For most users the **CLI** is simpler and safer. See:

- ``src/tooluniverse/database_setup/embedding_database.py``  
- ``src/tooluniverse/database_setup/embedding_sync.py``

.. admonition:: Tool JSONs you’ll see

   **tooluniverse/data/embedding_tools.json** — **real, loadable tools** for automation/agents  
   (``EmbeddingDatabase``, ``EmbeddingSync``). Load with:

   .. code-block:: python

      from tooluniverse.tool_universe import ToolUniverse
      tu = ToolUniverse()
      tu.load_tools(tool_config_files={"pkg": "tooluniverse/data/embedding_tools.json"})

   **docs/tools/generic_embedding_tool.json** — **example** that points the real
   ``EmbeddingCollectionSearchTool`` at *your* collection. Copy it, set
   ``"fields.collection"``, then load it:

   .. code-block:: python

      from tooluniverse.tool_universe import ToolUniverse
      tu = ToolUniverse()
      tu.load_tools(tool_config_files={"local": "docs/tools/generic_embedding_tool.json"})

``EmbeddingCollectionSearchTool`` is a **real ToolUniverse tool** (registered in code).
We don’t ship a pre-bound JSON for it because the collection name is yours. Use the example
JSON under ``docs/tools/``, set ``"fields.collection"`` to your collection (e.g., ``"toy"``),
and load it. If you prefer not to create a JSON, you can also instantiate the tool directly
from Python and pass the collection name via ``fields``.


Mini FAQ
--------

- **What’s “hybrid” search?** A smart mix of exact words + meaning. Start here.  
- **Do I need to set an embedding dimension?** No — it’s detected automatically.  
- **Changed models?** Rebuild; dimensions are auto-handled.  
- **Re-running build?** Safe. Duplicates (same ``doc_key``) are ignored; new text is added.  
- **“No results”?** Try ``--method keyword`` or confirm the ``--collection`` name.  
- **Where are my files stored locally?** ``<user_cache_dir>/embeddings/``. Examples:  
  - macOS → ``~/Library/Caches/ToolUniverse``  
  - Linux → ``~/.cache/tooluniverse``  
  - Windows → ``%LOCALAPPDATA%\\ToolUniverse``  
- **Where does my data upload?** ``tu-datastore sync-hf upload`` targets your **own** HF account by default (based on your token).  
- **Can I upload my tool JSON with the datastore?** Yes — pass one or more files via ``--tool-json`` during ``sync-hf upload``; they’re stored at the dataset root.
- **How do I pull tool JSONs too?** Use ``--include-tools`` with ``sync-hf download`` to download any ``*.json`` in the dataset.
- **Is upload private by default?** Yes auto upload **private** datasets unless you opt out (CLI: ``--no-private``; tool: set ``"private": false``).
- **Do I have to pass --db to search/build?**  
  - No — both commands write and read from your cache automatically.  
  - Use `--db` only if you want a **custom output path** (for example, a shared directory).  
  - When using the **JSON tool** or agents, no paths are ever needed — everything resolves automatically from the collection name.

Deeper reference (for the curious)
----------------------------------

- CLI: ``src/tooluniverse/database_setup/cli.py``  
- Content store / keyword search (FTS5): ``src/tooluniverse/database_setup/sqlite_store.py``  
- Vector index (FAISS): ``src/tooluniverse/database_setup/vector_store.py``  
- Embedding providers: ``src/tooluniverse/database_setup/embedder.py``  
- Hybrid retrieval: ``src/tooluniverse/database_setup/search.py``  
- Build/search orchestration: ``src/tooluniverse/database_setup/pipeline.py``  
- Model/dimension utils: ``src/tooluniverse/database_setup/embed_utils.py``  
- HF upload/download helpers: ``src/tooluniverse/database_setup/hf/sync_hf.py``  
- ToolUniverse search tool: ``src/tooluniverse/database_setup/generic_embedding_search_tool.py``  
- Tool example you can copy/edit: ``docs/tools/generic_embedding_tool.json`` (for reference)

With these steps, your data is searchable, agent-ready, and shareable—powering everything from quick local tests to fully reproducible, public ToolUniverse tools.