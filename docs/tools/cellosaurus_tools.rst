Cellosaurus Tools
=================

The Cellosaurus tools provide comprehensive access to the Cellosaurus database, a knowledge resource on cell lines. These tools enable searching, querying, and retrieving detailed information about cell lines using natural language queries and structured API calls.

Overview
--------

Cellosaurus is a knowledge resource on cell lines that provides information on cell lines from major cell line collections worldwide. The tools integrate with the official Cellosaurus API to provide:

- **Search functionality**: Find cell lines using natural language or structured queries
- **Query conversion**: Convert natural language queries to Solr syntax for precise searches
- **Detailed information retrieval**: Get comprehensive information about specific cell lines

Available Tools
---------------

cellosaurus_search_cell_lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Search Cellosaurus cell lines using the official API endpoint.

**Parameters:**
- ``q`` (string, required): Search query. Supports Solr syntax for field-specific searches
- ``offset`` (integer, optional): Number of results to skip for pagination (default: 0)
- ``size`` (integer, optional): Maximum number of results to return (default: 20)

**Example Usage:**
.. code-block:: python

    # Basic search
    result = tool.run({"q": "HeLa"})
    
    # Field-specific search
    result = tool.run({"q": "id:HeLa AND ox:9606"})
    
    # Pagination
    result = tool.run({"q": "cancer", "offset": 20, "size": 10})

**Response:**
Returns a dictionary with:
- ``success``: Boolean indicating if the search was successful
- ``results``: Dictionary containing cell_lines, total, offset, and size
- ``query``: The search query that was executed
- ``error``: Error message if the search failed

cellosaurus_query_converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert natural language queries to Solr syntax for precise Cellosaurus API searches.

**Parameters:**
- ``query`` (string, required): Natural language query to convert
- ``include_explanation`` (boolean, optional): Whether to include detailed explanation (default: true)

**Example Usage:**
.. code-block:: python

    # Simple conversion
    result = tool.run({"query": "human cancer cells"})
    
    # Complex query
    result = tool.run({"query": "HeLa cells from lung tissue"})
    
    # Without explanation
    result = tool.run({"query": "mouse cell lines", "include_explanation": False})

**Response:**
Returns a dictionary with:
- ``success``: Boolean indicating if the conversion was successful
- ``original_query``: The original natural language query
- ``solr_query``: The converted Solr query
- ``is_valid``: Whether the generated Solr query is valid
- ``validation_message``: Validation message for the Solr query
- ``explanation``: Detailed explanation of the conversion process (if requested)
- ``error``: Error message if conversion failed

cellosaurus_get_cell_line_info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get detailed information about a specific cell line using its Cellosaurus accession number.

**Parameters:**
- ``accession`` (string, required): Cellosaurus accession number (must start with 'CVCL_')
- ``format`` (string, optional): Response format - 'json', 'xml', 'txt', or 'fasta' (default: 'json')
- ``fields`` (list, optional): Specific fields to retrieve (e.g., ['id', 'ox', 'char'])

**Example Usage:**
.. code-block:: python

    # Get all information
    result = tool.run({"accession": "CVCL_0030"})
    
    # Get specific fields
    result = tool.run({
        "accession": "CVCL_0030",
        "fields": ["id", "ox", "char", "site"]
    })
    
    # Get in different format
    result = tool.run({
        "accession": "CVCL_0030",
        "format": "xml"
    })

**Response:**
Returns a dictionary with:
- ``success``: Boolean indicating if the request was successful
- ``accession``: The requested accession number
- ``data``: Cell line data (structure depends on format and fields requested)
- ``format``: The response format
- ``error``: Error message if request failed

Field Reference
---------------

The Cellosaurus API supports many fields for precise searching. Here are some key fields:

**Basic Information:**
- ``id``: Recommended name of the cell line
- ``sy``: List of synonyms
- ``ac``: Primary accession number
- ``ox``: Species (NCBI taxon identifier)
- ``sx``: Sex of the donor
- ``ag``: Age at sampling time

**Characteristics:**
- ``char``: Production process or biological properties
- ``site``: Body part (tissue or organ) derived from
- ``cell``: Cell type derived from
- ``ca``: Category (cancer, hybridoma, etc.)

**Disease and Health:**
- ``di``: Disease(s) suffered by the donor
- ``prob``: Known problems (contaminated, misidentified, etc.)

**References:**
- ``ref``: Publication references
- ``rx``: Publication cross-references

**Technical:**
- ``time``: Population doubling time
- ``kar``: Karyotype information
- ``str``: Short tandem repeat profile

For a complete list of all 60+ available fields, see the `Cellosaurus API Fields documentation <https://api.cellosaurus.org/api-fields>`_.

Workflow Examples
-----------------

**Complete Workflow: Natural Language to Detailed Information**

.. code-block:: python

    # Step 1: Convert natural language to Solr
    converter = CellosaurusQueryConverterTool(tool_config={})
    conversion_result = converter.run({"query": "human cancer cells from lung"})
    
    if conversion_result.get('success'):
        solr_query = conversion_result.get('solr_query')
        
        # Step 2: Search using converted query
        searcher = CellosaurusTool(tool_config={})
        search_result = searcher.run({"q": solr_query, "size": 5})
        
        if search_result.get('success'):
            cell_lines = search_result.get('results', {}).get('cell_lines', [])
            
            # Step 3: Get detailed info for each cell line
            info_tool = CellosaurusGetCellLineInfoTool(tool_config={})
            for cell_line in cell_lines:
                accession_data = cell_line.get('ac', [])
                if accession_data:
                    accession = accession_data[0].get('data', '')
                    if accession:
                        info_result = info_tool.run({"accession": accession})
                        # Process detailed information

**Field-Specific Searches**

.. code-block:: python

    # Search by species
    result = tool.run({"q": "ox:9606"})  # Human cell lines
    
    # Search by tissue type
    result = tool.run({"q": "site:lung"})
    
    # Search by disease
    result = tool.run({"q": "di:cancer"})
    
    # Combined search
    result = tool.run({"q": "ox:9606 AND site:lung AND char:cancer"})

**Error Handling**

.. code-block:: python

    result = tool.run({"q": "HeLa"})
    
    if result.get('success'):
        # Process successful result
        cell_lines = result.get('results', {}).get('cell_lines', [])
    else:
        # Handle error
        error_message = result.get('error')
        print(f"Search failed: {error_message}")

Installation and Setup
----------------------

The Cellosaurus tools are part of the ToolUniverse ecosystem. To use them:

1. Install ToolUniverse
2. Import the tools from the tooluniverse package
3. Create tool instances with appropriate configuration

.. code-block:: python

    from tooluniverse.cellosaurus_tool import (
        CellosaurusTool,
        CellosaurusQueryConverterTool,
        CellosaurusGetCellLineInfoTool
    )
    
    # Create tool instances
    search_tool = CellosaurusTool(tool_config={})
    converter_tool = CellosaurusQueryConverterTool(tool_config={})
    info_tool = CellosaurusGetCellLineInfoTool(tool_config={})

Configuration
-------------

The tools support configuration through environment variables:

- ``CELLOSAURUS_TIMEOUT``: Request timeout in seconds (default: 30)

API Rate Limits
---------------

The Cellosaurus API is free to use but may have rate limits. The tools include timeout handling and error management to work within these limits.

For more information about the Cellosaurus database and API, visit:
- `Cellosaurus Database <https://web.expasy.org/cellosaurus/>`_
- `Cellosaurus API Documentation <https://api.cellosaurus.org/>`_
- `Cellosaurus API Fields <https://api.cellosaurus.org/api-fields>`_
