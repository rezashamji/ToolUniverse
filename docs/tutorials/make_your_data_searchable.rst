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
AZURE_OPENAI_ENDPOINT=[https://YOUR_RESOURCE.openai.azure.com/](https://YOUR_RESOURCE.openai.azure.com/)
OPENAI_API_VERSION=2024-12-02 #example
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

Once you’ve built a collection (for example, `toy`), the next step is to **make it searchable through ToolUniverse** — either for yourself, inside an agent, or as a shared public tool.

Before we start, here’s the mental model:

* A **Tool** performs a specific function — like searching your collection.
* An **Agent** decides *which* tools to call to answer a question.
* **ToolUniverse** connects them all: it loads tools, manages data, and runs agents.

You can connect your collection in **three levels of integration** depending on your goal:

1. **Run it directly in Python** — quick local testing.
2. **Add it to your own agent** — dynamic use in your custom scripts.
3. **Register it permanently (JSON)** — auto-load it in every ToolUniverse session and prepare it for team or public sharing.

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

**Option B: Add it to your own agent (dynamic use)**
```

.. code-block:: python

from tooluniverse.agent import ToolUniverseAgent
from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

agent = ToolUniverseAgent()
search_tool = EmbeddingCollectionSearchTool(
tool_config={"fields": {"collection": "toy"}}
)
agent.register_tool(search_tool)

response = agent.run("Find entries about glucose in the toy collection.")
print(response)

**Use this when:** you’re developing a custom agent that reasons and calls tools automatically.
This registration only affects that single agent while your code is running.

---

**Option C: Register it permanently (JSON for agents + sharing)**

```

If you’d like your collection to be **available every time ToolUniverse —or any agent— starts**,  
save its definition as a **JSON file**. ToolUniverse scans these JSONs on startup, registers the tools automatically, and makes them callable by any agent.

Save this as, for example, ``docs/tools/generic_embedding_tool.json``:

.. code-block:: json

   {
     "name": "EmbeddingCollectionSearchTool",
     "type": "EmbeddingCollectionSearchTool",
     "fields": {
       "collection": "toy"
     }
   }

Place it either in ``docs/tools/`` or in ``src/tooluniverse/data/``.

When ToolUniverse launches, it will:

* **Register your tool automatically** – it appears in every agent’s tool list.  
* **Make it reproducible** – anyone with the same JSON can load it identically.  
* **Integrate with Hugging Face uploads** – the tool points to the same collection name (``toy``) that others can later download.  
* **Follow the ecosystem standard** – every shared ToolUniverse tool (public or private) uses JSON definitions.

**Use this when:** you want your tool to load automatically each time you open ToolUniverse — ideal for consistent setups, collaborative teams, or preparing your collection for public release.

💡 **Note:** This registers the *tool definition* locally.  
To share the actual *data* (``toy.db`` and ``toy.faiss``) with others, upload it to Hugging Face.

---

Back up or share your collection (Hugging Face)
-----------------------------------------------

If you followed **Option C**, this is the final step for making your collection *public-ready.*

ToolUniverse can sync your local datastore (the ``.db`` and ``.faiss`` files) directly with your Hugging Face account, so anyone can download and use the same dataset you built.

Note: Uploading requires a Hugging Face *write token* tied to your account.  
Downloading from public repos does not require a token.

**To upload your collection:**

.. code-block:: bash

   tu-datastore sync-hf upload --collection toy

When you run this command:

* It uses your ``HF_TOKEN`` to find your username automatically.  
* The data is stored in your personal namespace (e.g., ``username/toy``).  
* The collection’s `.db` and `.faiss` files are uploaded to Hugging Face Datasets.  

Optionally, you can override the repo name or make it private:

.. code-block:: bash

   tu-datastore sync-hf upload \
       --collection toy \
       --repo "username/my-toy-db" \
       --private

**To download from any public repo:**

.. code-block:: bash

   tu-datastore sync-hf download \
       --repo "username/my-toy-db" \
       --collection toy \
       --overwrite

If the repo is private, only users with permission (or a valid ``HF_TOKEN``) can download it.

Once uploaded, anyone who downloads both your **collection files** and your **JSON tool definition** will have a complete, ready-to-use ToolUniverse tool — the same one your agents can call automatically.

---

**Summary: Choosing the right option**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------------------+----------------------------------------------+---------------------------------------------+
| **Your goal**                              | **How to do it**                            | **Who it’s for**                            |
+============================================+==============================================+=============================================+
| Just test or explore your data             | Run ``tool.run({...})`` in Python           | Analysts, first-time users                  |
+--------------------------------------------+----------------------------------------------+---------------------------------------------+
| Build or extend your own agent             | ``agent.register_tool(search_tool)``         | Developers building custom agents           |
+--------------------------------------------+----------------------------------------------+---------------------------------------------+
| Keep it preloaded / prepare for release    | Save JSON in ``docs/tools/`` or ``src/tooluniverse/data/`` | Teams, reproducible or public projects |
+--------------------------------------------+----------------------------------------------+---------------------------------------------+
| Share your data publicly                   | ``tu-datastore sync-hf upload``              | Anyone publishing datasets or tools         |
+--------------------------------------------+----------------------------------------------+---------------------------------------------+

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
* ``src/tooluniverse/generic_embedding_search_tool.py`` — ToolUniverse-facing search tool definition  
* Tool configs: ``tooluniverse/data/embedding_tools.json`` and ``tooluniverse/data/generic_embedding_tool.json``  
* Tests: ``src/test/tests_database_setup/`` — run with ``pytest -q -m api``  

For a deeper understanding, start by reading through ``search.py`` and ``pipeline.py`` — they show exactly how hybrid search is implemented under the hood.

---

With these steps, your data is now searchable, agent-ready, and shareable — powering everything from quick local tests to fully reproducible, public ToolUniverse tools.
```
