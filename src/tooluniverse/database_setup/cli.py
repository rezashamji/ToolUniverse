"""
tu-datastore: CLI for building, searching, and syncing embedding datastores.

Subcommands
-----------
build
    Upsert a collection, insert documents (with de-dup), embed texts, and write FAISS.
search
    Run keyword / embedding / hybrid queries against an existing collection.
sync-hf upload|download
    Upload/download <collection>.db and <collection>.faiss to/from Hugging Face.

Env & credentials
-----------------
EMBED_PROVIDER, EMBED_MODEL and provider-specific keys (OPENAI / AZURE_* / HF_TOKEN).
HF_TOKEN is required for syncing private repos.

Exit codes
----------
0 on success; non-zero on I/O, validation, or runtime errors.
"""

import argparse
import json
import os
from .pipeline import build_collection
from .pipeline import search
from .hf.sync_hf import upload as sync_upload
from .hf.sync_hf import download as sync_download
from .packager import pack_folder
from .embed_utils import get_model_dim


def main():
    """Entry point for the `tu-datastore` CLI.

    Parses arguments and dispatches to:
    - pipeline.build_collection / pipeline.search for datastore operations
    - hf.sync_hf.upload / hf.sync_hf.download for Hugging Face synchronization
    """

    p = argparse.ArgumentParser("tu-datastore")
    sub = p.add_subparsers(dest="cmd")

    # build
    b = sub.add_parser("build", help="Build or extend a collection from docs")
    b.add_argument("--db", required=True)
    b.add_argument("--collection", required=True)
    b.add_argument(
        "--docs-json",
        required=True,
        help="Path to JSON list of [doc_key, text, metadata, optional_hash]",
    )
    b.add_argument("--provider", required=True)
    b.add_argument("--model", required=True)
    b.add_argument("--dim", required=True, type=int)

    # quickbuild
    qb = sub.add_parser(
        "quickbuild", help="Build a collection from a folder of .txt/.md"
    )
    qb.add_argument(
        "--name", required=True, help="Collection name (e.g., joe_guidelines)"
    )
    qb.add_argument("--from-folder", required=True, help="Folder containing .txt/.md")
    qb.add_argument(
        "--provider", help="Provider override (openai|azure|huggingface|local)"
    )
    qb.add_argument("--model", help="Model/deployment override")

    # search
    s = sub.add_parser("search", help="Search a collection")
    s.add_argument("--db", required=True)
    s.add_argument("--collection", required=True)
    s.add_argument("--query", required=True)
    s.add_argument(
        "--method", default="hybrid", choices=["keyword", "embedding", "hybrid"]
    )
    s.add_argument("--top-k", default=10, type=int)
    s.add_argument("--alpha", default=0.5, type=float)
    s.add_argument("--provider", help="Provider override for embedding/hybrid")
    s.add_argument("--model", help="Model override for embedding/hybrid")

    # sync-hf
    sh = sub.add_parser("sync-hf", help="Upload/download collection artifacts to HF")
    sh_sub = sh.add_subparsers(dest="action", required=True)

    up = sh_sub.add_parser("upload", help="Upload collection artifacts to HF")
    up.add_argument("--collection", required=True)
    up.add_argument("--repo", required=True)
    up.add_argument("--private", action="store_true")

    down = sh_sub.add_parser("download", help="Download collection artifacts from HF")
    down.add_argument("--repo", required=True)
    down.add_argument("--collection", required=True)
    down.add_argument("--overwrite", action="store_true")

    args = p.parse_args()

    if args.cmd == "build":
        with open(args.docs_json) as f:
            raw = json.load(f)
        # Normalize dict-style docs.json into 3–4 tuples
        docs = []
        for d in raw:
            if isinstance(d, dict):
                docs.append(
                    (
                        d["doc_key"],
                        d["text"],
                        d.get("metadata", {}),
                        d.get("text_hash"),  # may be None
                    )
                )
            else:
                docs.append(tuple(d))

        build_collection(
            args.db, args.collection, docs, args.provider, args.model, args.dim
        )

    elif args.cmd == "search":
        res = search(
            args.db,
            args.collection,
            args.query,
            method=args.method,
            top_k=args.top_k,
            alpha=args.alpha,
            embed_provider=args.provider,
            embed_model=args.model,
        )
        print(res)

    elif args.cmd == "sync-hf":
        if args.action == "upload":
            sync_upload(
                collection=args.collection, repo=args.repo, private=args.private
            )
        elif args.action == "download":
            sync_download(
                repo=args.repo,
                collection=args.collection,
                overwrite=args.overwrite,
            )

    elif args.cmd == "quickbuild":
        docs = pack_folder(args.from_folder)
        if not docs:
            raise SystemExit("No supported files found. Put .txt or .md in the folder.")
        
        # Fall back to environment if args not provided
        provider = args.provider or os.getenv("EMBED_PROVIDER")
        model = args.model or os.getenv("EMBED_MODEL")
        
        if not provider or not model:
            raise SystemExit(
                "Missing embedding provider or model. Please specify --provider and --model, "
                "or set EMBED_PROVIDER and EMBED_MODEL environment variables."
            )

        # Derive dim automatically
        dim = get_model_dim(provider=provider, model=model)
        build_collection(
            db_path="data/embeddings/{}.db".format(args.name),
            collection=args.name,
            docs=docs,
            embed_provider=provider,
            embed_model=model,
            embed_dim=dim,
        )
        print(f"Built collection '{args.name}' with {len(docs)} docs.")

    else:
        p.print_help()
