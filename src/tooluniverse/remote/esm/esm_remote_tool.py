"""
ESM Remote MCP Tool (FastMCP-native)

Exposes ESM-C protein sequence embeddings over MCP.
"""

from fastmcp import FastMCP

from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein, LogitsConfig

# -----------------------------------------------------------------------------
# MCP server
# -----------------------------------------------------------------------------

mcp = FastMCP("ESM Embedding MCP Server")

# -----------------------------------------------------------------------------
# Global model cache
# -----------------------------------------------------------------------------

_ESM_CLIENT = None


def get_client():
    global _ESM_CLIENT
    if _ESM_CLIENT is None:
        _ESM_CLIENT = ESMC.from_pretrained("esmc_300m")
        _ESM_CLIENT.eval()
    return _ESM_CLIENT


# -----------------------------------------------------------------------------
# CORE LOGIC (CALLABLE LOCALLY + BY MCP)
# -----------------------------------------------------------------------------

def compute_embedding(sequence: str):
    """
    Core embedding logic (pure Python, callable locally).
    """
    client = get_client()

    protein = ESMProtein(sequence=sequence)
    tensor = client.encode(protein)

    output = client.logits(
        tensor,
        LogitsConfig(return_embeddings=True)
    )

    return output.embeddings[0].tolist()


# -----------------------------------------------------------------------------
# MCP TOOL
# -----------------------------------------------------------------------------

@mcp.tool(
    name="esm_embed_sequence",
    description="Generate protein sequence embeddings using ESM-C",
)
def esm_embed_sequence(sequence: str):
    embedding = compute_embedding(sequence)
    return {
        "model": "esmc_300m",
        "embedding_dim": len(embedding),
        "embedding": embedding,
    }


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # 🚀 START MCP SERVER
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8008,
    )
