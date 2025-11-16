.. _compact_mode_guide:

Compact Mode Guide
==================

Compact mode exposes only 4 core tools instead of 750+ tools, reducing context window usage by ~99% while maintaining full functionality.

What is Compact Mode?
---------------------

When enabled, compact mode exposes only 4 essential tools instead of all 750+ tools. All tools are still accessible via ``execute_tool``.

**Benefits:**
- 99% reduction in exposed tools (4 vs 750+)
- Full functionality maintained
- Ideal for AI agents with limited context windows

Core Tools
----------

1. **``list_tools``** - List available tools (names, categories, etc.)
2. **``grep_tools``** - Search tools by text/regex pattern
3. **``get_tool_info``** - Get tool information (description or full definition)
4. **``execute_tool``** - Execute any ToolUniverse tool by name

Quick Start
-----------

Command Line
~~~~~~~~~~~~

.. code-block:: bash

   # STDIO mode (for Claude Desktop)
   tooluniverse-smcp-stdio --compact-mode

   # HTTP mode
   tooluniverse-smcp-server --compact-mode --port 8000

Claude Desktop Configuration
----------------------------

Add to ``~/Library/Application Support/Claude/claude_desktop_config.json``:

.. code-block:: json

   {
     "mcpServers": {
       "tooluniverse-compact": {
         "command": "python",
         "args": [
           "-m", "tooluniverse.smcp_server",
           "--transport", "stdio",
           "--compact-mode"
         ],
         "env": {
           "FASTMCP_NO_BANNER": "1",
           "PYTHONWARNINGS": "ignore"
         }
       }
     }
   }

Usage
-----

In Claude Desktop, just configure the server and start using tools. Claude will automatically discover and call them.

**Typical workflow:**
1. Use ``list_tools(mode="names")`` to see available tools
2. Use ``grep_tools(pattern="...")`` to search for tools
3. Use ``get_tool_info(tool_names="...")`` to get details
4. Use ``execute_tool(tool_name="...", arguments={...})`` to execute tools

Comparison
----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Normal Mode
     - Compact Mode
   * - Tools Exposed
     - ~750 tools
     - 4 tools
   * - Context Usage
     - High
     - Low (99% reduction)
   * - Functionality
     - Full
     - Full (via execute_tool)

When to Use
-----------

**Use Compact Mode when:**
- Working with AI agents (Claude Desktop, etc.)
- Context window is limited

**Use Normal Mode when:**
- Context window is not a concern
- You want direct access to all tools

Examples
--------

See ``examples/compact_mode/`` for complete examples.

Related Documentation
---------------------

- :doc:`mcp_support` - General MCP support
- :doc:`building_ai_scientists/claude_desktop` - Claude Desktop integration
