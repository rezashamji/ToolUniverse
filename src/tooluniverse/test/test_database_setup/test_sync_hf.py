import os
import pytest
import numpy as np
from pathlib import Path

from tooluniverse.database_setup.sqlite_store import SQLiteStore
from tooluniverse.database_setup.vector_store import VectorStore
from tooluniverse.database_setup.hf.sync_hf import upload, download

@pytest.mark.hf
def test_hf_upload_download(tmp_path):
    token = os.getenv("HF_TOKEN")
    repo = os.getenv("HF_REPO")
    if not token or not repo:
        pytest.skip("Set HF_TOKEN and HF_REPO to run HF sync test")

    data_dir = tmp_path / "data" / "embeddings"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = str(data_dir / "demo.db")

    store = SQLiteStore(db_path)
    store.upsert_collection("demo", description="Demo", embedding_model="test", embedding_dimensions=4)
    store.insert_docs("demo", [("demo-1", "Hypertension demo text", {"topic": "bp"}, "hash-demo")])
    doc_id = store.fetch_docs("demo", doc_keys=["demo-1"])[0]["id"]

    vectors = VectorStore(db_path)
    vectors.load_index("demo", dim=4)
    vec = np.array([[0.1, 0.2, 0.3, 0.4]], dtype="float32")
    vectors.add_embeddings("demo", [doc_id], vec, dim=4)

    upload(collection="demo", repo=repo, private=True, commit_message="CI demo upload")

    Path(db_path).unlink(missing_ok=True)
    (data_dir / "demo.faiss").unlink(missing_ok=True)

    download(repo=repo, local_collection_name="demo", dest_dir=str(data_dir))
    assert Path(db_path).exists()
