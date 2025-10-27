"""
UniProt_search

Search UniProtKB database using flexible query syntax. Supports gene names (e.g., 'gene:TP53'), p...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def UniProt_search(
    query: str,
    organism: Optional[str] = None,
    limit: Optional[int] = None,
    fields: Optional[list[Any]] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search UniProtKB database using flexible query syntax. Supports gene names (e.g., 'gene:TP53'), p...

    Parameters
    ----------
    query : str
        Search query. Can be simple (e.g., 'MEIOB') or advanced ('gene:TP53 AND organ...
    organism : str
        Optional organism filter. Can use common name ('human') or taxonomy ID ('9606...
    limit : int
        Maximum number of results to return (default: 25, max: 500)
    fields : list[Any]
        Optional list of fields to return. Default returns: accession, id, protein_na...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "UniProt_search",
            "arguments": {
                "query": query,
                "organism": organism,
                "limit": limit,
                "fields": fields,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["UniProt_search"]
