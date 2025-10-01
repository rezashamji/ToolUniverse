Make Your Data Searchable: do it in minutes
============================================

1) Quick Demo
-------------

.. code-block:: bash

   # 0) Make sure your env is loaded once
   source .env

   # 1) Put two rows into demo.json
   printf '%s\n' \
   '[{"doc_key":"1","text":"Aspirin reduces pain.","metadata":{"tag":"drug"}},' \
   ' {"doc_key":"2","text":"Ibuprofen is an NSAID.","metadata":{"tag":"drug"}}]' > demo.json

   # 2) Build (creates data/embeddings/meds.db + meds.faiss + we auto-detect the dimension for you)
   DIM=$(python -m tooluniverse.database_setup.embed_utils get_model_dim --provider "$EMBED_PROVIDER" --model "$EMBED_MODEL")

   tu-datastore build --db data/embeddings/demo.db --collection meds \
     --docs-json demo.json --provider "$EMBED_PROVIDER" --model "$EMBED_MODEL" --dim $DIM

   # 3) Search (hybrid = best starting point)
   tu-datastore search --db data/embeddings/meds.db --collection meds \
     --query "pain relief" --method hybrid \
     --provider "$EMBED_PROVIDER" --model "$EMBED_MODEL"


2) Use a folder of files (no JSON needed)
-----------------------------------------

Put ``.txt`` or ``.md`` files in a folder:

.. code-block:: bash

   tu-datastore quickbuild --name notes --from-folder ./my_texts
   tu-datastore search --db data/embeddings/notes.db --collection notes \
     --query "project timeline" --method hybrid


3) Plug into a Tool
-------------------

Configure your tool:

* **Tool name**: ``EmbeddingCollectionSearchTool``
* **fields.collection**: your collection (e.g., ``notes``)
* **fields.db_path**: ``data/embeddings/notes.db`` (optional)

(Code snippet if helpful)

.. code-block:: python

   from tooluniverse.generic_embedding_search_tool import EmbeddingCollectionSearchTool
   tool = EmbeddingCollectionSearchTool(
     tool_config={"fields":{"collection":"notes","db_path":"data/embeddings/notes.db"}}
   )
   print(tool.run({"query":"timeline", "method":"hybrid", "top_k":5}))


Tiny Troubleshooting
--------------------

* **“No results”** → Try ``--method keyword`` for exact terms; confirm ``--collection`` matches what you built.
* **Azure errors** → ``EMBED_MODEL`` must be your **deployment name**.
* **Changed models** → Use a new collection name, or delete the existing ``.faiss`` file before rebuilding so dimensions match.
* **Add more data** → Append to your JSON and re-run the same ``build`` command (same collection name).


Learn More (Optional)
---------------------

* Internals: ``src/tooluniverse/database_setup/`` (each file has clear docstrings).
* Hugging Face sync: ``src/tooluniverse/database_setup/hf/sync_hf.py``.
* Tool configs: ``tooluniverse/data/embedding_tools.json``, ``tooluniverse/data/generic_embedding_tool.json``.
* Tests as runnable demos: ``src/test/tests_database_setup/``.

For most users: stick to the steps above.  
For devs/researchers: peek at ``search.py`` and ``pipeline.py`` to see how it’s wired.

