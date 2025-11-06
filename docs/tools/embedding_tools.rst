Embedding Tools
===============

**Configuration File**: ``embedding_tools.json``
**Tool Type**: Local
**Tools Count**: 6

This page contains all tools defined in the ``embedding_tools.json`` configuration file.

Available Tools
---------------

**embedding_database_add** (Type: EmbeddingDatabase)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add new documents to an existing embedding database. Generates embeddings for new documents using...

.. dropdown:: embedding_database_add tool specification

   **Tool Information:**

   * **Name**: ``embedding_database_add``
   * **Type**: ``EmbeddingDatabase``
   * **Description**: Add new documents to an existing embedding database. Generates embeddings for new documents using the same model as the original database and appends them to the existing FAISS index.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to add documents to existing database

   * ``database_name`` (string) (required)
     Name of the existing database to add documents to

   * ``documents`` (array) (required)
     List of new document texts to embed and add

   * ``metadata`` (array) (optional)
     Optional metadata for each new document (same length as documents)

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_database_add",
          "arguments": {
              "database_name": "example_value",
              "documents": ["item1", "item2"]
          }
      }
      result = tu.run(query)


**embedding_database_create** (Type: EmbeddingDatabase)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new embedding database from a collection of documents. Generates embeddings using OpenAI...

.. dropdown:: embedding_database_create tool specification

   **Tool Information:**

   * **Name**: ``embedding_database_create``
   * **Type**: ``EmbeddingDatabase``
   * **Description**: Create a new embedding database from a collection of documents. Generates embeddings using OpenAI or Azure OpenAI models and stores them in a searchable database with FAISS vector index and SQLite metadata storage.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to create database from documents

   * ``database_name`` (string) (required)
     Name for the new database (must be unique)

   * ``documents`` (array) (required)
     List of document texts to embed and store

   * ``metadata`` (array) (optional)
     Optional metadata for each document (same length as documents)

   * ``model`` (string) (optional)
     OpenAI/Azure OpenAI embedding model to use

   * ``description`` (string) (optional)
     Optional description for the database

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_database_create",
          "arguments": {
              "database_name": "example_value",
              "documents": ["item1", "item2"]
          }
      }
      result = tu.run(query)


**embedding_database_load** (Type: EmbeddingDatabase)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load an existing embedding database from a local path or external source. Allows importing databa...

.. dropdown:: embedding_database_load tool specification

   **Tool Information:**

   * **Name**: ``embedding_database_load``
   * **Type**: ``EmbeddingDatabase``
   * **Description**: Load an existing embedding database from a local path or external source. Allows importing databases created elsewhere or backed up databases into the current ToolUniverse instance.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to load database from external source

   * ``database_path`` (string) (required)
     Path to the existing database directory or file

   * ``database_name`` (string) (required)
     Local name to assign to the loaded database

   * ``overwrite`` (boolean) (optional)
     Whether to overwrite existing database with same name

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_database_load",
          "arguments": {
              "database_path": "example_value",
              "database_name": "example_value"
          }
      }
      result = tu.run(query)


**embedding_database_search** (Type: EmbeddingDatabase)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Search for semantically similar documents in an embedding database. Uses OpenAI embeddings to con...

.. dropdown:: embedding_database_search tool specification

   **Tool Information:**

   * **Name**: ``embedding_database_search``
   * **Type**: ``EmbeddingDatabase``
   * **Description**: Search for semantically similar documents in an embedding database. Uses OpenAI embeddings to convert query text to vectors and performs similarity search using FAISS with optional metadata filtering.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to search the database

   * ``database_name`` (string) (required)
     Name of the database to search in

   * ``query`` (string) (required)
     Query text to find similar documents for

   * ``top_k`` (integer) (optional)
     Number of most similar documents to return

   * ``filters`` (object) (optional)
     Optional metadata filters to apply to search results

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_database_search",
          "arguments": {
              "database_name": "example_value",
              "query": "example_value"
          }
      }
      result = tu.run(query)


**embedding_sync_download** (Type: EmbeddingSync)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download an embedding database from HuggingFace Hub to local storage. Allows accessing databases ...

.. dropdown:: embedding_sync_download tool specification

   **Tool Information:**

   * **Name**: ``embedding_sync_download``
   * **Type**: ``EmbeddingSync``
   * **Description**: Download an embedding database from HuggingFace Hub to local storage. Allows accessing databases shared by others or your own backups.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to download database from HuggingFace

   * ``repository`` (string) (required)
     HuggingFace repository to download from (format: username/repo-name)

   * ``local_name`` (string) (optional)
     Local name for the downloaded database (optional, defaults to repo name)

   * ``overwrite`` (boolean) (optional)
     Whether to overwrite existing local database with same name

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_sync_download",
          "arguments": {
              "repository": "example_value"
          }
      }
      result = tu.run(query)


**embedding_sync_upload** (Type: EmbeddingSync)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload a local embedding database to HuggingFace Hub for sharing and collaboration. Creates a dat...

.. dropdown:: embedding_sync_upload tool specification

   **Tool Information:**

   * **Name**: ``embedding_sync_upload``
   * **Type**: ``EmbeddingSync``
   * **Description**: Upload a local embedding database to HuggingFace Hub for sharing and collaboration. Creates a dataset repository with the database files and metadata.

   **Parameters:**

   * ``action`` (string) (optional)
     Action to upload database to HuggingFace

   * ``database_name`` (string) (required)
     Name of the local database to upload

   * ``repository`` (string) (required)
     HuggingFace repository name (format: username/repo-name)

   * ``description`` (string) (optional)
     Description for the HuggingFace dataset

   * ``private`` (boolean) (optional)
     Whether to create a private repository

   * ``commit_message`` (string) (optional)
     Commit message for the upload

   **Example Usage:**

   .. code-block:: python

      query = {
          "name": "embedding_sync_upload",
          "arguments": {
              "database_name": "example_value",
              "repository": "example_value"
          }
      }
      result = tu.run(query)


Navigation
----------

* :doc:`tools_config_index` - Back to Tools Overview
* :doc:`../guide/loading_tools` - Loading Local Tools
