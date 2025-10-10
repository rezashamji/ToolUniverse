Tool Caller Tutorial
==================

The Tool Caller is the primary execution engine in ToolUniverse. It is responsible for instantiating tools, validating requests, and dispatching calls. Upon initialization, the Tool Caller is configured with a manifest of available tools, including their specifications and settings. To mitigate the significant system overhead associated with loading all tools simultaneously, it employs a dynamic loading strategy. A specific tool is loaded into memory only upon its first request and is then cached for a duration to efficiently handle subsequent calls.

When a tool execution request is received, the Tool Caller first parses it to extract the tool name and arguments. It then performs a rigorous validation check, ensuring the provided arguments conform to the data types and structural requirements defined in the tool's specification. Once validated, the Tool Caller dispatches the arguments to the tool's primary execution method, such as ``run()``. The resulting output is then returned to the client through ToolUniverse's communication protocols. If any step in this process fails, from loading to validation or execution, the system generates and returns a descriptive error message.

This Tutorial covers the main approaches to using the Tool Caller:

1. **Direct API Usage**: Using ToolUniverse's Python API to call tools programmatically
2. **MCP Server Integration**: Setting up and using MCP (Model Context Protocol) servers for AI agent integration

Direct API Usage
----------------

The ToolUniverse class provides the core Tool Caller functionality through its execution methods.

Basic Tool Execution
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tooluniverse import ToolUniverse

   # Initialize ToolUniverse
   tu = ToolUniverse()
   tu.load_tools()

   # Execute a single tool using the main run method
   result = tu.run({
       "name": "UniProt_get_entry_by_accession",
       "arguments": {"accession": "P05067"}
   })

   print(result)

The ``run`` method is the primary execution engine that handles both single and multiple function calls.

.. seealso::
   For complete API documentation, see :doc:`api_comprehensive` - ToolUniverse class and methods

Tool Initialization and Caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools are dynamically loaded and cached for performance:

.. seealso::
   For complete API documentation, see :doc:`api_comprehensive` - ToolUniverse class and methods

Internal Execution Method
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``run`` method internally uses ``run_one_function`` for individual tool execution:

.. seealso::
   For complete API documentation, see :doc:`api_comprehensive` - ToolUniverse class and methods

.. note::
   While ``run_one_function`` is available for direct use, the ``run`` method is the recommended interface as it provides better error handling, supports multiple function calls, and offers more flexible input parsing options.

Advanced Tool Execution
~~~~~~~~~~~~~~~~~~~~~~~

The ``run`` method supports various input formats and execution modes:

.. code-block:: python

   # Execute single function call (dictionary format)
   result = tu.run({
       "name": "UniProt_get_entry_by_accession",
       "arguments": {"accession": "P05067"}
   })

   # Execute multiple function calls (list format)
   result = tu.run([
       {
           "name": "UniProt_get_entry_by_accession",
           "arguments": {"accession": "P05067"}
       },
       {
           "name": "OpenTargets_get_associated_targets_by_disease_efoId",
           "arguments": {"efoId": "EFO_0000249"}
       }
   ])

   # Execute with formatted messages (for AI agent integration)
   result = tu.run(function_call_data, return_message=True, verbose=True)

   # Execute with different parsing formats
   result = tu.run(function_call_string, format='llama', verbose=True)

Tool Validation
~~~~~~~~~~~~~~~

The Tool Caller performs comprehensive validation before execution:

.. seealso::
   For complete API documentation, see :doc:`api_comprehensive` - ToolUniverse class and methods

.. _mcp-server-integration:

MCP Server Integration
----------------------

ToolUniverse provides comprehensive MCP (Model Context Protocol) server capabilities through the SMCP (Scientific Model Context Protocol) implementation. This allows AI agents to discover and execute tools through a standardized protocol.

SMCP Server Overview
~~~~~~~~~~~~~~~~~~~~

The SMCP server extends standard MCP capabilities with scientific domain expertise, intelligent tool discovery, and optimized configurations for research applications. It automatically handles the complex task of exposing hundreds of specialized tools through a consistent, well-documented interface.

.. seealso::
   For complete SMCP API documentation, see :doc:`api_comprehensive` - SMCP class

Key Features:
- **Scientific Tool Integration**: Native access to 350+ specialized tools
- **AI-Powered Tool Discovery**: Multi-tiered intelligent search system
- **Full MCP Protocol Support**: Complete implementation of MCP specification
- **High-Performance Architecture**: Production-ready features

Server Setup
~~~~~~~~~~~~

Python Configuration
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from tooluniverse.smcp import SMCP

   # Create a basic MCP server
   server = SMCP(
       name="Scientific Research Server",
       tool_categories=["uniprot", "opentarget", "ChEMBL"],
       search_enabled=True,
       max_workers=10
   )

   # Start the server
   server.run_simple(
       transport="http",
       host="localhost",
       port=8000
   )

Command Line Setup
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Start MCP server with specific configuration
   tooluniverse-smcp \
       --port 8000 \
       --host 0.0.0.0 \
       --categories "uniprot" "opentarget" "ChEMBL" \
       --max-workers 10 \
       --verbose

   # List all available tools
   tooluniverse-smcp --list-tools

   # List available categories
   tooluniverse-smcp --list-categories

Complete Parameter Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: Complete SMCP Command Line Parameters

   The ``tooluniverse-smcp`` command supports the following parameters:

   **Tool Selection:**
   - ``--categories``: Load specific tool categories (e.g., uniprot ChEMBL opentarget)
   - ``--include-tools``: Load only specific tools by name
   - ``--exclude-tools``: Exclude specific tools by name
   - ``--exclude-categories``: Exclude entire tool categories
   - ``--tools-file``: Load tools from a text file (one tool name per line)

   **Server Configuration:**
   - ``--transport``: Transport protocol (stdio, http, sse) - default: http
   - ``--host``: Host to bind to - default: 0.0.0.0
   - ``--port``: Port to bind to - default: 7000
   - ``--name``: Server name - default: "ToolUniverse SMCP Server"
   - ``--max-workers``: Maximum worker threads - default: 5
   - ``--no-search``: Disable intelligent search functionality
   - ``--verbose``, ``-v``: Enable verbose logging

   **Information Commands:**
   - ``--list-tools``: List all available tools and exit
   - ``--list-categories``: List all available tool categories and exit

.. seealso::
   For complete SMCP server documentation, see :doc:`../tutorials/aiscientists/adding_mcp_tools_en`

.. _mcp-client-integration:

MCP Client Integration
~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: Python MCP Client Examples

   **STDIO Client:**

   .. code-block:: python

      from mcp.client.stdio import stdio_client
      from mcp.client.session import ClientSession
      from mcp import StdioServerParameters
      import asyncio

      async def connect_to_tooluniverse():
          # Create stdio server parameters
          server_params = StdioServerParameters(
              command="tooluniverse-smcp-stdio",
              args=[]
          )

          # Create stdio client transport
          async with stdio_client(server_params) as (read, write):
              # Create client session
              async with ClientSession(read, write) as session:
                  # Initialize the session
                  await session.initialize()

                  # List available tools
                  tools_result = await session.list_tools()
                  print(f"Available tools: {len(tools_result.tools)}")

                  # Call a tool
                  result = await session.call_tool(
                      "UniProt_get_entry_by_accession",
                      {"accession": "P05067"}
                  )

                  return result

      # Run the client
      result = asyncio.run(connect_to_tooluniverse())

   **HTTP Client:**

   .. code-block:: python

      from mcp.client.session import ClientSession
      from mcp.client.streamable_http import streamablehttp_client
      import asyncio

      async def connect_via_http():
          # Connect to HTTP MCP server
          async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, get_session_id):
              async with ClientSession(read, write) as session:
                  await session.initialize()

                  # List available tools
                  tools_result = await session.list_tools()
                  print(f"Available tools: {len(tools_result.tools)}")

                  # Call a tool
                  result = await session.call_tool(
                      "UniProt_get_entry_by_accession",
                      {"accession": "P05067"}
                  )

                  return result

      # Run the client
      result = asyncio.run(connect_via_http())

.. dropdown:: cURL Client Examples

   You can also interact with ToolUniverse MCP servers directly using cURL commands:

   .. code-block:: bash

      # List available tools
      curl -X POST http://localhost:8000/mcp \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{
          "jsonrpc": "2.0",
          "id": 1,
          "method": "tools/list",
          "params": {}
        }'

      # Call a tool
      curl -X POST http://localhost:8000/mcp \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{
          "jsonrpc": "2.0",
          "id": 2,
          "method": "tools/call",
          "params": {
            "name": "UniProt_get_entry_by_accession",
            "arguments": {
              "accession": "P05067"
            }
          }
        }'

.. seealso::
   For detailed MCP integration tutorials, see :doc:`../tutorials/aiscientists/adding_mcp_tools_en`

Important Notes for MCP Clients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Required Headers**: ToolUniverse MCP servers use the streamable-http protocol, which requires:
   - `Content-Type: application/json`
   - `Accept: application/json, text/event-stream`

2. **JSON-RPC 2.0 Format**: All requests must follow the JSON-RPC 2.0 specification with:
   - `jsonrpc: "2.0"`
   - `id`: Unique request identifier
   - `method`: The MCP method to call
   - `params`: Method parameters

3. **Tool Arguments**: When calling tools, arguments must match the tool's parameter schema exactly.

Tool Execution Flow
-------------------

The Tool Caller follows a systematic execution flow:

1. **Request Parsing**: The ``run()`` method parses input and extracts function call data
2. **Format Detection**: Determines if input is single function call or multiple calls
3. **Tool Validation**: ``run_one_function()`` validates the tool exists and arguments are valid
4. **Dynamic Loading**: Load the tool if not already cached using ``init_tool()``
5. **Configuration Injection**: Inject necessary configurations (API keys, endpoints)
6. **Execution**: Call the tool's ``run()`` method
7. **Result Processing**: Format and return the result
8. **Error Handling**: Generate descriptive error messages if any step fails

For multiple function calls, the ``run()`` method iterates through each call and uses ``run_one_function()`` internally.

.. _error-handling-validation:

Error Handling and Validation
-----------------------------

The Tool Caller provides comprehensive error handling:

.. code-block:: python

   # Example error handling
   try:
       result = tu.run({
           "name": "nonexistent_tool",
           "arguments": {"param": "value"}
       })
   except Exception as e:
       print(f"Tool execution failed: {e}")

   # Validation errors
   invalid_call = {
       "name": "UniProt_get_entry_by_accession",
       "arguments": {"wrong_param": "value"}  # Missing required 'accession' parameter
   }

   result = tu.run(invalid_call)
   # Returns: "Invalid function call: Missing required parameter: accession"

.. _performance-optimization:

Performance Optimization
-------------------------

Dynamic Loading Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

The Tool Caller uses lazy loading to optimize performance:

- Tools are loaded only when first requested
- Loaded tools are cached for subsequent calls
- Memory usage is minimized by not loading all tools at startup
- Cache duration can be configured based on usage patterns

Thread Pool Execution
~~~~~~~~~~~~~~~~~~~~~

For MCP servers, tools execute in thread pools to prevent blocking:

.. code-block:: python

   # Configure thread pool size
   server = SMCP(
       max_workers=20,  # Adjust based on server capacity
       tool_categories=["uniprot", "opentarget"]
   )

.. _troubleshooting:

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

1. **Tool Not Found**: Ensure the tool name is correct and the tool is loaded
2. **Invalid Arguments**: Check that all required parameters are provided
3. **API Key Issues**: Verify that necessary API keys are configured
4. **Network Errors**: Check connectivity to external services
5. **Memory Issues**: Reduce the number of loaded tools or increase available memory

Debugging Tips
~~~~~~~~~~~~~~

.. dropdown:: Debugging and Troubleshooting

   **Enable Debug Logging:**

   .. code-block:: python

      # Enable debug logging
      from tooluniverse.logging_config import set_log_level
      set_log_level("DEBUG")

      # Check loaded tools
      print(f"Loaded tools: {len(tu.all_tools)}")
      print(f"Cached tools: {len(tu.callable_functions)}")

      # Validate tool configuration
      tool_config = tu.all_tool_dict.get("tool_name")
      if tool_config:
          print(f"Tool configuration: {tool_config}")

   **Common Issues and Solutions:**

   1. **Tool Not Found**: Ensure the tool name is correct and the tool is loaded
   2. **Invalid Arguments**: Check that all required parameters are provided
   3. **API Key Issues**: Verify that necessary API keys are configured
   4. **Network Errors**: Check connectivity to external services
   5. **Memory Issues**: Reduce the number of loaded tools or increase available memory

.. seealso::
   For comprehensive troubleshooting Tutorial, see :doc:`../help/troubleshooting`

Summary
-------

This comprehensive Tutorial covers both direct API usage and MCP server integration for the Tool Caller. The Tool Caller's dynamic loading strategy, validation system, and error handling make it a robust execution engine for ToolUniverse's extensive collection of scientific tools.

**Key Takeaways:**

- Use the ``run()`` method for all tool execution needs
- Tools are dynamically loaded and cached for optimal performance
- MCP servers provide standardized AI agent integration
- Comprehensive error handling and validation ensure reliable operation
- Debug logging and troubleshooting tools help resolve issues quickly

For more detailed information, refer to the :doc:`api_comprehensive` documentation and :doc:`tutorials/aiscientists/adding_mcp_tools_en` tutorials.

.. toctree::
   :hidden:

   tutorials/aiscientists/adding_mcp_tools_en
