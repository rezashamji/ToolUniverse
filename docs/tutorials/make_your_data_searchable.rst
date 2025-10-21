ToolUniverse Datastore: the 5-step guide to make your data searchable and incorporated as ToolUniverse tool
==========================================================================================================

Make your own text searchable (by exact words, by meaning, or both) and use it from tools.
All local collections are stored under `~/.cache/tooluniverse/embeddings/` by default.

What you’ll do
--------------

1. Install
2. Tell us which embedding service to use
3. Save your data (JSON)
4. Build a “collection” (your searchable library)
5. Search it, and (optional) use it from a Tool or back it up online


Helpful Terms
---------------------

* **Collection** = a named library of your texts (e.g., ``toy``, ``articles``).
* **doc_key** = your unique ID per row (e.g., ``art-101``).
* **text** = the content to search (a sentence, paragraph, or article).
* **metadata** = any extra info (title, tags, author). Optional.
* **``tu-datastore``** = the command you run in Terminal to build & search.

  Tip: ``doc_key`` must be **unique inside a collection**.


1) Install
----------

.. code-block:: bash

   # from the repo root
   python -m venv .venv && source .venv/bin/activate
   pip install tooluniverse

If you’re developing locally, use pip install -e . instead.


2) Choose ONE embedding service
-------------------------------

Create a file named **.env** in the repo root. Pick one block below (or multiple if planning to use several services), to input into the **.env** file then:

.. code-block:: bash

   source .env

**Azure OpenAI**

.. code-block:: bash

   EMBED_PROVIDER=azure
   AZURE_OPENAI_API_KEY=YOUR_KEY
   AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/
   OPENAI_API_VERSION=2024-12-01-preview # example (other versions available)
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


3) Put your data in a JSON file
-------------------------------

Save as .json file. Use objects with ``doc_key``, ``text``, and optional ``metadata``.

Here is an example, ``my.json``:

.. code-block:: json

   [
     {"doc_key":"d1","text":"Mitochondria is the powerhouse of the cell.","metadata":{"title":"Cells","tags":["Biology"]}},
     {"doc_key":"d2","text":"Insulin is a hormone regulating glucose.","metadata":{"title":"Endocrine","tags":["Medicine"]}}
   ]

  CSV isn’t a CLI input at the moment. If your data is a spreadsheet, export to CSV and convert to the JSON shape above (keep it simple: ``doc_key``, ``text``, and optional ``metadata``).


4) Build your collection
------------------------

Build:

.. code-block:: bash

   # choose a name, e.g. "toy" (you can have many collections)
   tu-datastore build \
   --db ~/.cache/tooluniverse/embeddings/toy.db \
   --collection toy \
   --docs-json my.json \
   --provider "$EMBED_PROVIDER" \
   --model "$EMBED_MODEL"

What this does: creates a small database (`~/.cache/tooluniverse/embeddings/toy.db`) and a FAISS index (`toy.faiss`) so your texts can be found by words and by meaning.
The embedding dimension is detected automatically. No extra parameters needed.

  Alternative (no JSON): put `.txt`/`.md` files in a folder and run:

  .. code-block:: bash

     # uses EMBED_PROVIDER and EMBED_MODEL from your .env
     tu-datastore quickbuild --name toy --from-folder ./my_texts

     # or override explicitly
     tu-datastore quickbuild --name toy --from-folder ./my_texts \
       --provider azure --model text-embedding-3-small

It automatically detects the embedding dimension and builds `~/.cache/tooluniverse/embeddings/toy.db` + `toy.faiss`.

5) Search your collection
-------------------------

Pick one (you can try all three):

.. code-block:: bash

   # exact words
   tu-datastore search --db ~/.cache/tooluniverse/embeddings/toy.db --collection toy \
   --query glucose --method keyword

   # fuzzy meaning (uses your embedding service)
   tu-datastore search --db ~/.cache/tooluniverse/embeddings/toy.db --collection toy \
   --query glucose --method embedding \
   --provider "$EMBED_PROVIDER" --model "$EMBED_MODEL"

   # best of both (recommended)
   tu-datastore search --db ~/.cache/tooluniverse/embeddings/toy.db --collection toy \
   --query glucose --method hybrid \
   --provider "$EMBED_PROVIDER" --model "$EMBED_MODEL" --alpha 0.5

**Example result:**

.. code-block:: json

   [
     {
       "doc_id": 2,
       "doc_key": "d2",
       "text": "Insulin is a hormone regulating glucose.",
       "metadata": {"title":"Endocrine","tags":["Medicine"]},
       "score": 0.83
     }
   ]


Plug your data into a Tool
------------------------------------

If you’re wiring this into a ToolUniverse agent, configure your tool:

* **Tool name**: ``EmbeddingCollectionSearchTool``
* **fields.collection**: ``toy``
* **fields.db_path**: `~/.cache/tooluniverse/embeddings/toy.db` (optional; defaults to that path)

.. code-block:: python

   from tooluniverse.database_setup.generic_embedding_search_tool import EmbeddingCollectionSearchTool

   tool = EmbeddingCollectionSearchTool(
      tool_config={"fields": {"collection": "toy", "db_path": "~/.cache/tooluniverse/embeddings/toy.db"}}
   )
   results = tool.run({"query": "glucose", "method": "hybrid", "top_k": 5})
   print(results)

You can also define this tool directly in JSON form to register it in ToolUniverse.

An example configuration file is provided here:
``docs/tools/generic_embedding_tool.json``

This example shows how to specify the tool type, collection name, search parameters,
and required fields for a basic embedding search tool.


(Optional) Back up or share online (Hugging Face)
-------------------------------------------------

Note: Uploading requires a Hugging Face *write token* tied to your account. 
Downloading from public repos does not require a token.

 You can upload and share your datastore directly through your **own Hugging Face account**.

 When you run `tu-datastore sync-hf upload`, it uses your `HF_TOKEN` to determine your username automatically.
 The data is stored in your personal namespace (e.g., `username/collection`).

 **To upload:**

 ```bash
 tu-datastore sync-hf upload --collection toy
 ```

 *(Optional)* You can override the repo name or make it private:

 ```bash
 tu-datastore sync-hf upload --collection toy --repo "username/my-toy-db" --private
 ```

**To download from any public repo:**

```bash
tu-datastore sync-hf download --repo "username/my-toy-db" --collection toy --overwrite
```

**If the repo is private**, only users with permission (or a valid `HF_TOKEN`) can download it.

Mini FAQ
--------

* **What’s “hybrid” search?** A smart mix of exact words + meaning. Start there.
* **Where are my files?** In `~/.cache/tooluniverse/embeddings/` (e.g., `toy.db` and `toy.faiss`).
* **Azure tip:** ``EMBED_MODEL`` is your **deployment name**.
* **Changed model?** Just rebuild — the correct embedding dimension is detected automatically.* **Re-running build:** Safe. Duplicates (same ``doc_key``) are ignored; new text is added.
* **“No results”** → Try `--method keyword` for exact terms; confirm `--collection` matches what you built.
* **Add more data** → Append to your JSON and re-run the same `build` command (same collection name).
* **Where does my data upload?** `tu-datastore sync-hf upload` now uploads to **your** Hugging Face account by default, not to AgenticX.

Want to dig deeper?
-------------------

These are the exact files that implement what you just used:

* ``src/tooluniverse/database_setup/cli.py`` — ``tu-datastore`` commands (``build``, ``search``, ``quickbuild``, ``sync-hf``)
* ``src/tooluniverse/database_setup/sqlite_store.py`` — docs/metadata storage + keyword (FTS5)
* ``src/tooluniverse/database_setup/vector_store.py`` — FAISS index (cosine via L2+IP)
* ``src/tooluniverse/database_setup/embedder.py`` — OpenAI / Azure / HF / local
* ``src/tooluniverse/database_setup/search.py`` — hybrid scoring and retrieval
* ``src/tooluniverse/database_setup/pipeline.py`` — build/search helpers
* ``src/tooluniverse/database_setup/embed_utils.py`` — ``get_model_dim()`` and simple embedding
* ``src/tooluniverse/database_setup/hf/sync_hf.py`` — Hugging Face upload/download
* ``src/tooluniverse/generic_embedding_search_tool.py`` — ToolUniverse-facing search tool
* Tool configs: ``tooluniverse/data/embedding_tools.json``, ``tooluniverse/data/generic_embedding_tool.json``
* Tests: ``src/test/tests_database_setup/`` — run with ``pytest -q -m api``

For devs/researchers: peek at `search.py and pipeline.py to see how it’s wired.