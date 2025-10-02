"""
Hugging Face sync utilities for SQLite + FAISS datastore artifacts.

Artifacts
---------
- <collection>.db     : SQLite content store (docs, FTS5 mirror, metadata)
- <collection>.faiss  : FAISS index (IndexFlatIP), sibling to the DB under ./data/embeddings

Public API
----------
db_path_for_collection(collection) -> Path
    Resolve the on-disk SQLite path for a collection.

upload(collection, repo, private=True, commit_message="Update")
    Create/ensure a HF dataset repo and upload <collection>.db/.faiss.

download(repo, collection, overwrite=False)
    Download *.db/*.faiss from a HF dataset repo snapshot and restore them
    under ./data/embeddings as <collection>.db/.faiss.

Notes
-----
- Requires HF_TOKEN (env or HfFolder) for private repos or authenticated uploads.
- Upload streams large files; download uses huggingface_hub.snapshot_download.
- Existing local files are preserved unless overwrite=True.
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import HfApi, HfFolder, snapshot_download

# Always load .env if present
load_dotenv()

DATA_DIR = Path("./data/embeddings")
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------
# Helpers
# ---------------------------


def db_path_for_collection(collection: str) -> Path:
    """Return the absolute path for ``./data/embeddings/<collection>.db``."""
    return DATA_DIR / f"{collection}.db"


def get_hf_api():
    """Return an authenticated (HfApi, token) tuple.

    Raises
    ------
    RuntimeError
        If no token is available from HF_TOKEN or HfFolder.
    """

    token = os.getenv("HF_TOKEN") or HfFolder.get_token()
    if not token:
        raise RuntimeError("HF_TOKEN not set in environment or .env file")
    return HfApi(token=token), token


# ---------------------------
# Upload
# ---------------------------


def upload(
    collection: str, repo: str, private: bool = True, commit_message: str = "Update"
):
    """Upload a collection’s DB and FAISS index to a HF dataset repo.

    Parameters
    ----------
    collection : str
        Name of the local collection; resolves <collection>.db/.faiss under DATA_DIR.
    repo : str
        Dataset repo ID (e.g., "org/name").
    private : bool, default True
        Create/use a private repo when True.
    commit_message : str, default "Update"
        Commit message for the upload.

    Raises
    ------
    FileNotFoundError
        If <collection>.db does not exist locally.
    RuntimeError
        On missing/invalid auth.
    """

    api, token = get_hf_api()

    # Ensure repo exists
    api.create_repo(
        repo_id=repo, repo_type="dataset", private=private, exist_ok=True, token=token
    )

    # Upload SQLite DB
    db_path = db_path_for_collection(collection)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    api.upload_file(
        path_or_fileobj=str(db_path),
        path_in_repo=f"{collection}.db",
        repo_id=repo,
        repo_type="dataset",
        commit_message=commit_message,
        token=token,
    )

    # Upload FAISS index
    faiss_path = DATA_DIR / f"{collection}.faiss"
    if faiss_path.exists():
        api.upload_file(
            path_or_fileobj=str(faiss_path),
            path_in_repo=f"{collection}.faiss",
            repo_id=repo,
            repo_type="dataset",
            commit_message=commit_message,
            token=token,
        )
    else:
        print(f"No FAISS index found for {collection}")

    print(f"Uploaded {collection} to HF repo {repo}")


# ---------------------------
# Download
# ---------------------------

def download(repo: str, collection: str, overwrite: bool = False):
    """Download *.db/*.faiss from a HF dataset repo and restore them locally.

    Parameters
    ----------
    repo : str
        Dataset repo ID to pull from (e.g., "org/name").
    collection : str
        Base name to save as: produces <name>.db and <name>.faiss under DATA_DIR.
    overwrite : bool, default False
        Replace local files if they already exist.

    Notes
    -----
    - Chooses the first *.db and first *.faiss found in the snapshot.
    - Prints progress to stdout.
    """
    
    _, token = get_hf_api()

    snapshot_path = snapshot_download(
        repo_id=repo,
        repo_type="dataset",
        token=token,
    )

    snap = Path(snapshot_path)
    db_candidates = sorted(snap.glob("*.db"))
    faiss_candidates = sorted(snap.glob("*.faiss"))

    dest_db = db_path_for_collection(collection)
    dest_faiss = DATA_DIR / f"{collection}.faiss"

    if db_candidates:
        src_db = db_candidates[0]
        if overwrite or not dest_db.exists():
            shutil.copy(src_db, dest_db)
            print(f" Restored {dest_db.name} from {src_db.name}")
        else:
            print(f" {dest_db.name} already exists locally. Skipping (use --overwrite).")
    else:
        print(" No DB found in HF repo snapshot")

    if faiss_candidates:
        src_faiss = faiss_candidates[0]
        if overwrite or not dest_faiss.exists():
            shutil.copy(src_faiss, dest_faiss)
            print(f" Restored {dest_faiss.name} from {src_faiss.name}")
        else:
            print(f" {dest_faiss.name} already exists locally. Skipping (use --overwrite).")
    else:
        print(" No FAISS index found in HF repo snapshot")

    print(f" Download complete for {collection} from {repo}")


# ---------------------------
# Entrypoint
# ---------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Sync datastore collections with Hugging Face Hub"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Upload
    up = subparsers.add_parser("upload", help="Upload a collection to HF Hub")
    up.add_argument(
        "--collection", required=True, help="Collection name (e.g., euhealth, demo)"
    )
    up.add_argument("--repo", required=True, help="HF dataset repo ID")
    up.add_argument("--private", action="store_true", help="Make repo private")
    up.add_argument(
        "--commit_message", default="Update", help="Commit message for upload"
    )

    # Download
    down = subparsers.add_parser("download", help="Download a collection from HF Hub")
    down.add_argument("--repo", required=True, help="HF dataset repo ID")
    down.add_argument(
        "--collection",
        required=True,
        help="Local collection name (e.g., euhealth, demo)",
    )
    down.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing local DB/FAISS"
    )

    args = parser.parse_args()

    if args.command == "upload":
        upload(
            collection=args.collection,
            repo=args.repo,
            private=args.private,
            commit_message=args.commit_message,
        )
    elif args.command == "download":
        download(
            repo=args.repo,
            collection=args.collection,
            overwrite=args.overwrite,
        )
    else:
        parser.print_help()
