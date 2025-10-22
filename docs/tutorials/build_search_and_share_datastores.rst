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

Prepare your data (JSON)
------------------------

Save as ``.json`` with ``doc_key``, ``text``, and optional ``metadata``.

Example ``my.json``:

.. code-block:: json

   [
     {"doc_key":"d1","text":"Mitochondria is the powerhouse of the cell.","metadata":{"title":"Cells","tags":["Biology"]}},
     {"doc_key":"d2","text":"Insulin is a hormone regulating glucose.","metadata":{"title":"Endocrine","tags":["Medicine"]}}
   ]

CSV isn’t supported. If your data is in a spreadsheet, export to CSV and convert to the JSON shape above.
   
Build your collection
---------------------

You can create a searchable datastore from either text files or a JSON list of documents.

**Option 1: QuickBuild (recommended)**

.. code-block:: bash

   tu-datastore quickbuild --name toy --from-folder ./my_texts

Automatically:
- detects your embedding model and dimension from `.env`
- builds `<user_cache_dir>/embeddings/toy.db` + `toy.faiss`

**Option 2: Build from JSON**

.. code-block:: bash

   tu-datastore build --collection toy --docs-json my.json

Same result, but accepts structured JSON with `doc_key`, `text`, and optional `metadata`.

.. note::
   Advanced users can still override provider/model or choose a custom path:

   .. code-block:: bash

      tu-datastore build \
         --collection toy \
         --docs-json my.json \
         --provider openai \
         --model text-embedding-3-small \
         --db ~/.cache/tooluniverse/embeddings/custom.db


Try a search (CLI)
------------------

.. code-block:: bash

   DB=~/.cache/tooluniverse/embeddings/toy.db  # adjust for your OS
   # Exact words
   tu-datastore search --db "$DB" --collection toy --query glucose --method keyword
   # Meaning (embeddings)
   tu-datastore search --db "$DB" --collection toy --query glucose --method embedding
   # Hybrid (recommended): best of both (alpha 0=words only, 1=embeddings only)
   tu-datastore search --db "$DB" --collection toy --query glucose --method hybrid --alpha 0.5

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

Use your collection in ToolUniverse (recommended)
-------------------------------------------------

**Goal:** make your search callable by any ToolUniverse **agent**.  
You’ll create a small **JSON tool definition** and load it. That’s it.

**Meet the search tool (conceptual)**
   ToolUniverse has a built-in **search tool** that queries a collection you’ve built.
   Your JSON just tells ToolUniverse **which collection** to use and **what parameters** (query, method, etc.).
   You don’t need to wire up paths; it looks in ``<user_cache_dir>/embeddings/`` automatically.

1) Save a tool definition (example)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save as ``docs/tools/toy_search_tool.json``:

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
   tu.load_tools(tool_config_files={"local": "docs/tools/toy_search_tool.json"})

   # Now any agent (or you) can call:
   results = tu.tools.toy_search(query="glucose", method="hybrid", top_k=5)
   print(results)

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
   # or override destination / make private:
   tu-datastore sync-hf upload --collection toy --repo "username/my-toy-db" --private

**Download (works for public repos; private requires permission or a valid HF token):**

.. code-block:: bash

   tu-datastore sync-hf download --repo "username/my-toy-db" --collection toy --overwrite


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
- **Automating in CI or admin flows?** → Advanced automation tools (above).

Advanced: automation / CI (admins)
----------------------------------

For provisioning via agents/CI instead of the CLI, you also have registered tools:

- **EmbeddingDatabase** — programmatically build/update a collection  
- **EmbeddingSyncTool** — programmatically upload/download to Hugging Face

For most users the **CLI** is simpler and safer. See:

- ``src/tooluniverse/database_setup/embedding_database.py``  
- ``src/tooluniverse/database_setup/embedding_sync.py``

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
- Example tool JSON: ``docs/tools/generic_embedding_tool.json`` (for reference)

With these steps, your data is searchable, agent-ready, and shareable—powering everything from quick local tests to fully reproducible, public ToolUniverse tools.




# ToolUniverse Datastore: the 3-minute guide to make your data searchable and usable in ToolUniverse

Make your own text searchable (by exact words, by meaning, or both) and use it from tools.
All local collections are stored under `<user_cache_dir>/embeddings/` by default.

---

## What you’ll do

1. Install
2. Tell us which embedding service to use (OpenAI, Azure, or Hugging Face)
3. Save your data (JSON or text files)
4. Build a “collection” (your searchable library)
5. Search and/or use it inside an agent

---

## Helpful Terms

* **Collection** — a named library of your texts (e.g., `toy`, `articles`).
* **doc_key** — your unique ID per row (e.g., `art-101`).
* **text** — the content to search (a sentence, paragraph, or article).
* **metadata** — any extra info (title, tags, author). Optional.
* **`tu-datastore`** — the command you run in Terminal to build & search.

Tip: `doc_key` must be **unique inside a collection**.

---

1. Install

---

.. code-block:: bash

# from the repo root

python -m venv .venv && source .venv/bin/activate
pip install tooluniverse

If you’re developing locally, use `pip install -e .` instead.

---

2. Choose ONE embedding service

---

Create a file named **.env** in the repo root.
Pick one block below (or multiple if you plan to use several services), paste it into your **.env**, then run:

.. code-block:: bash

source .env

**Azure OpenAI**

.. code-block:: bash

   EMBED_PROVIDER=azure
   AZURE_OPENAI_API_KEY=YOUR_KEY
   AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/
   OPENAI_API_VERSION=2024-12-02  # example
   EMBED_MODEL=text-embedding-3-small   # your DEPLOYMENT name


**OpenAI**

.. code-block:: bash

EMBED_PROVIDER=openai
OPENAI_API_KEY=YOUR_KEY
EMBED_MODEL=text-embedding-3-small

**Hugging Face**

.. code-block:: bash

EMBED_PROVIDER=huggingface
HF_TOKEN=YOUR_TOKEN
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2 #example

---

3. Put your data in a JSON file

---

Save as `.json` with `doc_key`, `text`, and optional `metadata`.

Example `my.json`:

.. code-block:: json

[
   {"doc_key":"d1","text":"Mitochondria is the powerhouse of the cell.","metadata":{"title":"Cells","tags":["Biology"]}},
   {"doc_key":"d2","text":"Insulin is a hormone regulating glucose.","metadata":{"title":"Endocrine","tags":["Medicine"]}}
]

CSV isn’t supported. If your data is in a spreadsheet, export to CSV and convert to the JSON shape above (keep it simple: `doc_key`, `text`, and optional `metadata`).

---

4. Build your collection

---

.. code-block:: bash

# choose a name, e.g. "toy" (you can have many collections)

tu-datastore build --collection toy --docs-json my.json

This creates a small SQLite database (`toy.db`) and a FAISS index (`toy.faiss`) inside your cache folder so your texts can be searched by words and by meaning.

Alternative (no JSON): put `.txt` or `.md` files in a folder and run:

.. code-block:: bash

# uses EMBED_PROVIDER and EMBED_MODEL from your .env

tu-datastore quickbuild --name toy --from-folder ./my_texts

It automatically detects the embedding dimension and builds
`<user_cache_dir>/embeddings/toy.db` + `<user_cache_dir>/embeddings/toy.faiss`.

Tip: To rebuild embeddings from scratch, add `--overwrite`.

---

5. Search your collection

---

Try any of these — they return ranked search results from your collection:

.. code-block:: bash

# Exact keyword match

tu-datastore search --collection toy --query glucose --method keyword

# Semantic meaning (embedding search)

tu-datastore search --collection toy --query glucose --method embedding

# Hybrid (recommended: combines both)

tu-datastore search --collection toy --query glucose --alpha 0.5

**Example result:**

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

---

## Make your collection usable by ToolUniverse

Once you’ve built a collection (for example, `toy`), the next step is to **make it searchable through ToolUniverse** — either for yourself, inside an agent, or as a shared public tool if you want. you can just do the above if you want

Before we start, here’s the mental model:

* A **Tool** performs a specific function — like searching your collection.
* An **Agent** decides *which* tools to call to answer a question.
* **ToolUniverse** connects them all: it loads tools, manages data, and runs agents.

Meet the tool you’ll call
-------------------------
In practice, there’s one built-in search tool: ``EmbeddingCollectionSearchTool``.
You point it at a **collection name** and pass a **query** (plus optional ``method``/``top_k``/``alpha``).
It automatically looks under ``<user_cache_dir>/embeddings/<collection>.db`` and ``<collection>.faiss``
(the files created by ``tu-datastore build``/``quickbuild``).


You can connect your collection in **three levels of integration** depending on your goal:

1. **Run it directly in Python** — quick local testing.
2. **Add it to your own agent** — dynamic use in your custom scripts.
3. **Register it permanently (JSON)** — auto-load it in every ToolUniverse session and prepare it for team or public sharing.


Which path should I use?
------------------------
- Just want agents to use my data (team-friendly)? → **Option C (recommended)**.
- Trying it in a notebook or script, no agents yet? → **Option A** or **Option B**.
- Unsure? Start with **Option C**; you can still use it from Python via `tu.load_tools(...)`.

---

**Option A: Run it directly in Python (no agent)**

```

.. code-block:: python

   from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

   tool = EmbeddingCollectionSearchTool(
       tool_config={"fields": {"collection": "toy"}}
   )

   results = tool.run({
       "query": "glucose",
       "method": "hybrid",
       "top_k": 5
   })

   print(results)

**Use this when:** you want to test your collection or explore results manually in a notebook.  
This behaves exactly like:
``tu-datastore search --collection toy --query glucose --method hybrid``.

---
**Option B: Use your collection programmatically (temporary session registration)**

Option B is the “**use it right now in Python**” path.  
It’s meant for anyone who wants to interact with a searchable collection programmatically — whether you just built one using ``tu-datastore build`` or you’re trying out an example collection for the first time.  
You can use it to:

* test that your collection works,  
* get structured search results directly inside code, or  
* wire it into a custom app or script (like a chatbot, dashboard, or notebook).

It does **not** create or save new data, it simply lets you call your collection programmatically, get ranked search hits, and use those results however you want.

When you run the code below, ToolUniverse will print a confirmation that your tool was registered successfully, followed by your search results.

.. code-block:: python

   from tooluniverse.tool_universe import ToolUniverse
   from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

   tu = ToolUniverse()  # starts a session (no tools loaded yet)

   tool_cfg = {
       "name": "embedding_search",
       "type": "EmbeddingCollectionSearchTool",
       "fields": {"collection": "toy"},
       "parameter": {
           "type": "object",
           "properties": {
               "query":  {"type": "string",  "description": "Search text"},
               "method": {"type": "string",  "default": "hybrid",
                          "enum": ["keyword", "embedding", "hybrid"]},
               "top_k":  {"type": "integer", "default": 5}
           },
           "required": ["query"]
       },
   }

   tu.register_custom_tool(EmbeddingCollectionSearchTool, tool_config=tool_cfg)

   # Run a search directly from Python
   results = tu.tools.embedding_search(query="glucose", method="hybrid", top_k=5)
   print(results)

**Example output**

.. code-block:: text

   ℹ️  Custom tool 'EmbeddingCollectionSearchTool' registered successfully!
   [{'doc_key': 'd2', 'text': 'Insulin is a hormone regulating glucose.', 'score': 0.82, ...},
    {'doc_key': 'd1', 'text': 'Mitochondria is the powerhouse of the cell.', 'score': 0.17, ...}]

This output means:

* The tool was successfully registered for this Python process.  
* The list that follows shows your **search results**, ranked by similarity — highest first.  
* Each dictionary represents one document from your collection, including its text, metadata, and similarity score.  
* You can treat this list like a normal Python object: loop over it, print it nicely, filter it, or pass it into another part of your program.  
  For example, if you were writing a chatbot or analysis script, you could use the top result as the answer or context for a follow-up step.

**Use this when:** you want to **query or experiment with your collection directly in Python**,  
without needing to build a full app or publish anything yet.  
   Typical cases include:
   * exploring how your search results look,  
   * writing a short notebook or prototype that uses those results, or  
   * integrating retrieval into a personal or local workflow (like a chatbot or analysis helper).

This registration is **temporary** — it lasts only while your script or notebook is running.  
To make the tool load automatically in every ToolUniverse session or share it with others, use **Option C** instead.

**Notes**

* ``fields.collection`` must match a built collection (e.g., created via ``tu-datastore build --collection toy``).  
* The ``name`` you give in the config becomes the function name you’ll call from Python — e.g., if you set ``"name": "embedding_search"``, the function name is ``tu.tools.embedding_search(...)``.  
* The ``parameter`` block is optional but helps validate inputs and auto-generate documentation.  
* The printed list of results shows the **top matches** to your query — you can filter, display, or pass them to another tool or model.

---

**Option C: Register it permanently (JSON for agents + sharing)**

If you’d like your collection to be **available everywhere with one line of code**, save its definition as a **JSON file** and load it.  
This makes it available every time ToolUniverse starts. ToolUniverse can load these JSONs at startup (or manually through
``tu.load_tools``), register the tools automatically, and make them callable by any agent.

Save as, for example, ``docs/tools/generic_embedding_tool.json``:

.. code-block:: json

   {
     "name": "embedding_search",
     "type": "EmbeddingCollectionSearchTool",
     "fields": { "collection": "toy" },
     "parameter": {
       "type": "object",
       "properties": {
         "query":  { "type": "string",  "description": "Search text" },
         "method": { "type": "string",  "default": "hybrid", "enum": ["keyword", "embedding", "hybrid"] },
         "top_k":  { "type": "integer", "default": 5 }
       },
       "required": ["query"]
     }
   }

Load it from any script:

.. code-block:: python

   from tooluniverse.tool_universe import ToolUniverse

   tu = ToolUniverse()
   tu.load_tools(tool_config_files={
       "local": "docs/tools/generic_embedding_tool.json"   # path to your JSON
   })

   # Now it’s available exactly like in Option B:
   results = tu.tools.embedding_search(query="glucose", method="hybrid", top_k=5)
   print(results)

**Use this when:** you want your tool to load automatically each time you open ToolUniverse. It is the best way to create a clean, reproducible, load anywhere tool. Also great for sharing with teammates or the public.  
Pair this with ``tu-datastore sync-hf upload`` to share the actual FAISS/SQLite files (explained below).

*(If you ship JSON inside your package and call ``tu.load_tools()`` with those paths, it will also be picked up.  
There’s no implicit auto-scan of arbitrary folders.)*

When ToolUniverse launches, it will:

* **Register your tool automatically** – it appears in every agent’s tool list.  
* **Make it reproducible** – anyone with the same JSON can load it identically.  
* **Integrate with Hugging Face uploads** – the tool points to the same collection name (``toy``) that others can later download.  
* **Follow the ecosystem standard** – every shared ToolUniverse tool (public or private) uses JSON definitions.

💡 **Note:** This registers the *tool definition* locally.  
To share the actual *data* (``toy.db`` and ``toy.faiss``) with others, upload it to Hugging Face.

---


**Summary: Choosing the right option**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - **Your goal**
     - **How to do it**
     - **Who it’s for**
   * - Just test or explore your data
     - Run ``tool.run({...})`` in Python
     - Analysts, first-time users
   * - Build or extend your own agent
     - Register in a session with ``tu.register_custom_tool(...)`` and call it from your agent loop
     - Developers building custom agents
   * - Keep it preloaded / prepare for release
     - Save JSON in ``docs/tools/`` (and load with ``tu.load_tools(...tool_config_files=...)``)
     - Teams, reproducible or public projects
   * - Share your data publicly
     - ``tu-datastore sync-hf upload``
     - Anyone publishing datasets or tools

All three paths use the same hybrid FAISS + SQLite backend as ``tu-datastore search`` —  
so your results remain identical whether you test locally, run an agent, or publish a public tool.

---

Mini FAQ
--------

* **What’s “hybrid” search?** A smart mix of exact words + meaning. It blends keyword precision with semantic similarity — start here for most use cases.  
* **Azure tip:** ``EMBED_MODEL`` is your **deployment name** (not the base model name).  
* **Changed model?** Just rebuild — the correct embedding dimension is detected automatically.  
* **Re-running build:** Safe. Duplicates (same ``doc_key``) are ignored; new text is added.  
* **“No results”?** Try ``--method keyword`` for exact terms, or confirm that ``--collection`` matches what you built.  
* **Add more data:** Append to your JSON and re-run the same ``build`` command (same collection name).  
* **Where does my data upload?** ``tu-datastore sync-hf upload`` uploads to **your own Hugging Face account** by default (under your username).  
* **Where are my files stored locally?**  
  Inside ``<user_cache_dir>/embeddings/`` — for example:  
  * macOS → ``~/Library/Caches/ToolUniverse``  
  * Linux → ``~/.cache/tooluniverse``  
  * Windows → ``%LOCALAPPDATA%\ToolUniverse``  

You **don’t** need to create these folders manually; ToolUniverse creates them automatically the first time you run ``tu-datastore build`` or ``tu-datastore quickbuild``.

---

Want to dig deeper?
-------------------

If you want to understand how everything fits together, here are the key files behind what you just used:

* ``src/tooluniverse/database_setup/cli.py`` — CLI commands (``build``, ``search``, ``quickbuild``, ``sync-hf``)  
* ``src/tooluniverse/database_setup/sqlite_store.py`` — document & metadata storage (keyword FTS5)  
* ``src/tooluniverse/database_setup/vector_store.py`` — FAISS vector index (cosine similarity via L2/IP)  
* ``src/tooluniverse/database_setup/embedder.py`` — Embedding APIs (OpenAI, Azure, Hugging Face, local)  
* ``src/tooluniverse/database_setup/search.py`` — Hybrid retrieval logic (keyword + embedding fusion)  
* ``src/tooluniverse/database_setup/pipeline.py`` — Build/search orchestration helpers  
* ``src/tooluniverse/database_setup/embed_utils.py`` — ``get_model_dim()`` and embedding utilities  
* ``src/tooluniverse/database_setup/hf/sync_hf.py`` — Hugging Face upload/download functions  
* ``src/tooluniverse/database_setup/generic_embedding_search_tool.py`` — ToolUniverse-facing search tool definition  
* Tool configs: ``tooluniverse/data/embedding_tools.json`` and ``tooluniverse/data/generic_embedding_tool.json``  
* Tests: ``src/test/tests_database_setup/`` — run with ``pytest -q -m api``  

For a deeper understanding, start by reading through ``search.py`` and ``pipeline.py`` — they show exactly how hybrid search is implemented under the hood.

.. note::
   **Advanced (admins/CI): provision & distribute without the CLI**
   Agents can also call registered tools to build collections and sync to/from Hugging Face.
   For most users, the CLI remains the simplest and safest route.
   See: ``src/tooluniverse/database_setup/embedding_database.py`` and
   ``src/tooluniverse/database_setup/embedding_sync.py``.

---

With these steps, your data is now searchable, agent-ready, and shareable — powering everything from quick local tests to fully reproducible, public ToolUniverse tools.
```
