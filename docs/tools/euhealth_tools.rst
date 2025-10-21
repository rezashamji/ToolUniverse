EUHealth tools: find EU public-health datasets fast
====================================================

Use these tools to:

* **Search** public EU health datasets by topic (e.g., cancer, vaccination, obesity, mental health…)
* **Deep-dive** a dataset’s landing page to surface useful outgoing links (download portals, etc.)

You do **not** need to know about “embeddings,” “dimensions,” or FAISS. Everything is handled automatically.

The tools read from a local library (a small database + index)::

  <user_cache_dir>/embeddings/euhealth.db
  <user_cache_dir>/embeddings/euhealth.faiss


Quick start (recommended): use the prebuilt library
---------------------------------------------------

1. **Get a Hugging Face token** (free account).
   Copy it once (Settings → Access Tokens).

2. **Download the ready-to-use EUHealth library:**

.. code-block:: bash

  # download from your own or any public Hugging Face repo
  export HF_TOKEN=YOUR_HF_TOKEN
  tu-datastore sync-hf download \
    --repo "username/euhealth" \
    --collection euhealth \
    --overwrite

That’s it. The files land in ``<user_cache_dir>/embeddings/`` where the tools expect them.

  Don’t have a token or prefer not to make an account? Skip to “Build it yourself” below.

Tip:
If you previously uploaded your own copy of the EUHealth datastore (tu-datastore sync-hf upload --collection euhealth),
it lives at huggingface.co/<your_username>/euhealth.

Use it
------

Just talk to your agent in plain English. Examples:

* “**Find cancer datasets for Germany**.”
  → Agent uses the *euhealth cancer search* tool and returns a list.

* “**Show vaccination datasets in English**.”
  → Agent calls the vaccination topic tool with a language filter.

* “**Deep-dive the first 3 results and give me the best download links**.”
  → Agent calls the deep-dive tool to classify links from each dataset’s landing page
  (e.g., ``html_portal``, ``login_or_error``, etc.).

Behind the scenes, the agent uses the tools defined in:
``src/tooluniverse/data/euhealth_tools.json``
(20 topics are pre-wired; you don’t have to touch this.)


Optional: quick terminal “smoke test”
-------------------------------------

If you want to sanity-check from Terminal (no coding):

.. code-block:: bash

   # Keyword search (works without any API keys)
  tu-datastore search \
    --collection euhealth \
    --query cancer \
    --method keyword \
    --top-k 5


You should see a few JSON results (uuid, title, landing_page, etc.).
(Inside the agent you’ll get nicely formatted results—this is just a quick check.)


Build it yourself (only if you can’t use the prebuilt)
------------------------------------------------------

If you can’t download from Hugging Face, you can build locally. You’ll need any one of:

* **OpenAI** (simplest): ``OPENAI_API_KEY``, ``EMBED_PROVIDER=openai``, ``EMBED_MODEL=text-embedding-3-small``
* **Azure OpenAI**: ``AZURE_OPENAI_API_KEY``, ``AZURE_OPENAI_ENDPOINT``, ``OPENAI_API_VERSION``
* **Hugging Face**: ``HF_TOKEN``, ``EMBED_PROVIDER=huggingface``, ``EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2``

Then run:

.. code-block:: bash

   # pick one provider, for example OpenAI:
   export EMBED_PROVIDER=openai
   export EMBED_MODEL=text-embedding-3-small
   export OPENAI_API_KEY=YOUR_KEY

   # build (crawl the portal, normalize, embed, index)
   python -m tooluniverse.euhealth.euhealth_live

This writes the same two files to ``<user_cache_dir>/embeddings/``.
Re-running is safe; it adds new items and skips duplicates.

  You never need to provide an “embedding dimension” or any extra parameters. It’s automatically detected based on your model and provider.

What each tool returns
----------------------

**Topic search tools** (e.g., cancer, vaccination, mental health) return a list of:

.. code-block:: json

   {
     "uuid": "…",
     "title": "…",
     "landing_page": "https://…",
     "license": "…",
     "keywords": ["…"],
     "themes": ["…"],
     "language": ["…"],
     "spatial": "…",
     "snippet": "first ~280 chars of text"
   }

**Deep-dive tool** (for selected datasets) returns:

.. code-block:: json

   {
     "uuid": "…",
     "title": "…",
     "landing_page": "…",
     "candidates": [
       {
         "url": "…",
         "classification": "html_portal | login_or_error | error",
         "http_status": 200,
         "content_type": "text/html",
         "notes": "…"
       }
     ]
   }


Common questions
----------------

* **Do I need to configure anything in code?**
  No. The tools are already registered. If the library exists in ``<user_cache_dir>/embeddings/``, you can just ask the agent.

* **Can I filter by country/language?**
  Yes—just say it (“Germany”, “DE”, “English”, “en”). The tools accept both plain names and codes.

* **What if some links say ``login_or_error``?**
  Some portals require accounts or block automated requests. The tool still shows you what’s there.

* **My agent says the EUHealth library isn’t found.**
  Make sure the files exist at::

    <user_cache_dir>/embeddings/euhealth.db
    <user_cache_dir>/embeddings/euhealth.faiss

  If not, use the **Quick start** download or the **Build it yourself** step.

* **Where does my data upload now?**
   When you run `tu-datastore sync-hf upload`, it uploads to **your Hugging Face account** (based on your `HF_TOKEN`).
   The `--repo` flag is optional. If omitted, it defaults to `<username>/<collection>`.


(Optional, for maintainers) Keep it fresh weekly
------------------------------------------------

We include a GitHub Actions workflow that rebuilds and uploads the library each week.

* File: ``.github/workflows/euhealth-cache-weekly-refresh.yml``
* It runs the live builder and then:

.. code-block:: bash

  # upload to your own Hugging Face repo by default
   tu-datastore sync-hf upload \
     --collection euhealth \
     --private

* You’ll need to add secrets for your chosen provider (e.g., ``OPENAI_API_KEY``) and ``HF_TOKEN``.

Most users can ignore this; it’s just for keeping the dataset library up to date.


You’re set
----------

* Prefer the **Quick start** download.
* Ask the agent normal questions (“Find cancer datasets in Germany”).
* Use **deep-dive** when you want the actual outgoing links.

If you later want the nitty-gritty (how we crawl, embed, index), see the developer notes in:
``src/tooluniverse/euhealth/*`` and ``src/tooluniverse/database_setup/*``.
