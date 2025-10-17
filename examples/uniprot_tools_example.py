#!/usr/bin/env python3
"""
UniProt Tools Example

Demonstrates various UniProt database tools available in ToolUniverse
"""

from tooluniverse import ToolUniverse
from typing import Any, Dict, List

# =============================================================================
# Tool Initialization
# =============================================================================
# Description: Initialize ToolUniverse and load all available tools
# Syntax: tu = ToolUniverse(); tu.load_tools()
tu = ToolUniverse()
tu.load_tools()

# =============================================================================
# Test Data Setup
# =============================================================================
# Description: Define test accession number for UniProt protein queries
# Note: P05067 is the accession for A4_HUMAN (Amyloid-beta precursor protein)
TEST_ACC = "P05067"  # A4_HUMAN

# =============================================================================
# Method 1: Basic Protein Information Retrieval
# =============================================================================
# Description: Get comprehensive protein entry information
# Syntax: tu.run({"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "P05067"}})
result1 = tu.run({"name": "UniProt_get_entry_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 2: Protein Function Information
# =============================================================================
# Description: Retrieve specific functional information about the protein
# Syntax: tu.run({"name": "UniProt_get_function_by_accession", "arguments": {"accession": "P05067"}})
result2 = tu.run({"name": "UniProt_get_function_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 3: Protein Naming Information
# =============================================================================
# Description: Get recommended and alternative names for the protein
# Syntax: tu.run({"name": "UniProt_get_recommended_name_by_accession", "arguments": {"accession": "P05067"}})
result3 = tu.run({"name": "UniProt_get_recommended_name_by_accession", "arguments": {"accession": TEST_ACC}})

# Alternative names
result4 = tu.run({"name": "UniProt_get_alternative_names_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 4: Organism and Localization Information
# =============================================================================
# Description: Get organism and subcellular location information
# Syntax: tu.run({"name": "UniProt_get_organism_by_accession", "arguments": {"accession": "P05067"}})
result5 = tu.run({"name": "UniProt_get_organism_by_accession", "arguments": {"accession": TEST_ACC}})

# Subcellular location
result6 = tu.run({"name": "UniProt_get_subcellular_location_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 5: Disease and Variant Information
# =============================================================================
# Description: Retrieve disease associations and genetic variants
# Syntax: tu.run({"name": "UniProt_get_disease_variants_by_accession", "arguments": {"accession": "P05067"}})
result7 = tu.run({"name": "UniProt_get_disease_variants_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 6: Post-Translational Modifications
# =============================================================================
# Description: Get information about PTMs and processing
# Syntax: tu.run({"name": "UniProt_get_ptm_processing_by_accession", "arguments": {"accession": "P05067"}})
result8 = tu.run({"name": "UniProt_get_ptm_processing_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 7: Sequence Information
# =============================================================================
# Description: Retrieve protein sequence data
# Syntax: tu.run({"name": "UniProt_get_sequence_by_accession", "arguments": {"accession": "P05067"}})
result9 = tu.run({"name": "UniProt_get_sequence_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Method 8: Isoform Information
# =============================================================================
# Description: Get information about protein isoforms
# Syntax: tu.run({"name": "UniProt_get_isoform_ids_by_accession", "arguments": {"accession": "P05067"}})
result10 = tu.run({"name": "UniProt_get_isoform_ids_by_accession", "arguments": {"accession": TEST_ACC}})

# =============================================================================
# Helper Function for Result Formatting
# =============================================================================
# Description: Utility function to format different types of results
# Note: This function helps understand the structure of returned data
def format_value(value, max_items=5, max_length=200):
    """Helper function to format output values with more detail"""
    if isinstance(value, dict):
        dict_str = str(value)
        return f"Dict ({len(dict_str)} chars): {dict_str[:500]}{'...' if len(dict_str) > 500 else ''}"
    elif isinstance(value, list):
        if not value:
            return "Empty list"
        items_to_show = value[:max_items]
        items_str = "\n  - ".join(
            [
                str(item)[:max_length] + ("..." if len(str(item)) > max_length else "")
                for item in items_to_show
            ]
        )
        remaining = len(value) - max_items
        return f"List with {len(value)} items:\n  - {items_str}" + (
            f"\n  ... and {remaining} more items" if remaining > 0 else ""
        )
    elif isinstance(value, str):
        return f"String ({len(value)} chars): {value[:max_length]}{'...' if len(value) > max_length else ''}"
    else:
        return f"Type: {type(value)}, Value: {value}"

# =============================================================================
# Error Handling Example
# =============================================================================
# Description: Demonstrate how to handle errors in UniProt queries
# Syntax: Check for error responses and handle appropriately
try:
    # Example with potentially invalid accession
    error_result = tu.run({"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "INVALID"}})
    if isinstance(error_result, dict) and "error" in error_result:
        # Handle error case
        pass
except Exception as e:
    # Handle exception case
    pass

# =============================================================================
# Summary of UniProt Tools
# =============================================================================
# Available UniProt tools provide comprehensive protein information:
# - Basic entry information and metadata
# - Functional annotations and descriptions
# - Naming conventions (recommended and alternative names)
# - Organism and taxonomic information
# - Subcellular localization data
# - Disease associations and genetic variants
# - Post-translational modifications
# - Protein sequence data
# - Isoform information
# 
# All tools use the same basic pattern:
# tu.run({"name": "tool_name", "arguments": {"accession": "P05067"}})
# 
# Results can be dictionaries, lists, or strings depending on the tool
# Error handling should check for "error" key in dictionary responses