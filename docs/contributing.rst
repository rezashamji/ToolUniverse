Contributing to ToolUniverse
============================

We welcome contributions to ToolUniverse! This guide covers both general contributions and specialized tool contributions.

Quick Start
-----------

1. Fork and clone the repository
2. Set up development environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ./setup_precommit.sh

3. Make your changes and test:

.. code-block:: bash

   pytest
   black src/tooluniverse/
   flake8 src/tooluniverse/

4. Submit a pull request

Development Standards
---------------------

Code Style
~~~~~~~~~~

- Use Black for formatting: ``black src/tooluniverse/``
- Follow PEP 8 guidelines
- Include type hints for all new code
- Write comprehensive docstrings

Testing
~~~~~~~

- Write tests for all new functionality
- Aim for >90% test coverage
- Run tests with: ``pytest --cov=tooluniverse``

Documentation
~~~~~~~~~~~~~

- Document all public APIs
- Include usage examples
- Update guides for new features
- Use Google-style docstrings

Tool Contributions
------------------

Adding New Tools
~~~~~~~~~~~~~~~~

ToolUniverse supports both local and remote tools. Here's how to add a new tool:

**Important**: When adding a new tool, you must modify ``src/tooluniverse/__init__.py`` in four specific locations to ensure the tool is properly exposed and importable. This step is critical and often overlooked by contributors.

Required __init__.py Modifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For every new tool class you add, you must update ``src/tooluniverse/__init__.py`` in these four locations:

1. **Add tool class declarations** (around lines 105-165): Add type annotations for your tool class
2. **Add import statements** (around lines 173-258): Import your tool class in the non-lazy loading section
3. **Add lazy import proxies** (around lines 260-360): Create lazy import proxy for your tool class
4. **Add tool names to __all__ list** (around lines 362-449): Add your tool class name to the ``__all__`` list

Example: Adding a new tool called ``MyNewTool``

.. code-block:: python

   # 1. Add class declaration (around line 165)
   MyNewTool: Any

   # 2. Add import statement (around line 258, in the non-lazy loading section)
   from .my_new_tool import MyNewTool

   # 3. Add lazy import proxy (around line 360, in the else block)
   MyNewTool = _LazyImportProxy("my_new_tool", "MyNewTool")

   # 4. Add to __all__ list (around line 449)
   __all__ = [
       # ... existing tools ...
       "MyNewTool",
   ]

**Validation Steps**: After making these changes, verify your tool is properly exposed by testing:

.. code-block:: python

   from tooluniverse import MyNewTool  # Should work without errors
   print(MyNewTool)  # Should show the class or lazy proxy

Local Tool Example
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from tooluniverse.tool_registry import register_tool
   from typing import Dict, Any

   @register_tool('MyTool', config={
       "name": "my_tool",
       "type": "MyTool",
       "description": "Tool description",
       "parameter": {
           "type": "object",
           "properties": {
               "input": {
                   "type": "string",
                   "description": "Input parameter"
               }
           },
           "required": ["input"]
       },
       "examples": [
           {
               "description": "Example usage",
               "arguments": {"input": "example_value"}
           }
       ],
       "tags": ["category", "subcategory"],
       "author": "Your Name <your.email@example.com>",
       "version": "1.0.0",
       "license": "MIT"
   })
   class MyTool:
       """Tool description."""

       def __init__(self, tool_config=None):
           self.tool_config = tool_config or {}

       def run(self, arguments):
           """Execute tool."""
           try:
               input_value = arguments["input"]
               # Your tool logic here
               result = self._process(input_value)
               return {"result": result, "success": True}
           except Exception as e:
               return {"error": str(e), "success": False}

       def _process(self, input_value):
           """Process input."""
           return {"processed": input_value}

Remote Tool Example
^^^^^^^^^^^^^^^^^^^

For remote tools, create an MCP server:

.. code-block:: python

   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from typing import Dict, Any

   app = FastAPI(title="My Tool MCP Server")

   class ToolRequest(BaseModel):
       input: str
       options: Dict[str, Any] = {}

   class ToolResponse(BaseModel):
       success: bool
       result: Dict[str, Any]
       error: str = None

   @app.post("/process", response_model=ToolResponse)
   async def process_request(request: ToolRequest):
       """Process tool request."""
       try:
           # Your tool logic here
           result = {"processed": request.input}
           return ToolResponse(success=True, result=result)
       except Exception as e:
           return ToolResponse(success=False, result={}, error=str(e))

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)

Then create a client configuration file:

.. code-block:: json

   {
       "tools": [
           {
               "name": "my_remote_tool",
               "type": "MyRemoteTool",
               "description": "Remote tool description",
               "parameter": {
                   "type": "object",
                   "properties": {
                       "input": {
                           "type": "string",
                           "description": "Input parameter"
                       }
                   },
                   "required": ["input"]
               },
               "settings": {
                   "server_url": "http://localhost:8000",
                   "timeout": 30,
                   "retries": 3
               },
               "tags": ["category", "remote"],
               "author": "Your Name <your.email@example.com>",
               "version": "1.0.0",
               "license": "MIT"
           }
       ]
   }

Complete Tool Development Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When adding a new tool, follow this complete workflow to ensure proper integration:

1. **Create your tool file** in ``src/tooluniverse/tools/`` (e.g., ``my_new_tool.py``)
2. **Implement your tool class** following the BaseTool interface
3. **Modify __init__.py** (critical step - see Required __init__.py Modifications above)
4. **Create comprehensive tests** in ``tests/unit/`` or ``tests/integration/``
5. **Add documentation** in ``docs/tools/``
6. **Update tool registry** if using custom registration
7. **Test the complete integration** to ensure your tool is properly exposed

**Step-by-step __init__.py modification checklist**:

.. code-block:: bash

   # 1. Add class declaration (find the section around line 105-165)
   # Look for: "MonarchTool: Any" and add your tool after similar entries
   
   # 2. Add import statement (find the non-lazy loading section around line 173-258)
   # Look for: "from .restful_tool import MonarchTool" and add your import
   
   # 3. Add lazy import proxy (find the else block around line 260-360)
   # Look for: "MonarchTool = _LazyImportProxy("restful_tool", "MonarchTool")" and add yours
   
   # 4. Add to __all__ list (find the __all__ list around line 362-449)
   # Add your tool name as a string in the list

**Common mistakes to avoid**:
- Forgetting to add the tool to all four locations
- Adding the import in the wrong section (lazy vs non-lazy)
- Incorrect module name in the lazy import proxy
- Missing quotes around the tool name in the __all__ list
- Not testing the import after making changes

Testing Your Tool
~~~~~~~~~~~~~~~~~

Create tests for your tool:

.. code-block:: python

   import pytest
   from tooluniverse.my_tool import MyTool

   class TestMyTool:
       def setup_method(self):
           self.tool = MyTool()

       def test_success(self):
           """Test successful execution."""
           result = self.tool.run({"input": "test_value"})
           assert result["success"] is True
           assert "processed" in result["result"]

       def test_error(self):
           """Test error handling."""
           result = self.tool.run({"input": ""})
           assert result["success"] is False
           assert "error" in result

Documentation
~~~~~~~~~~~~~

Create documentation for your tool:

.. code-block:: rst

   My Tool
   =======

   Tool description and features.

   Usage
   -----

   .. code-block:: python

      from tooluniverse import ToolUniverse

      tu = ToolUniverse()
      tu.load_tools()

      result = tu.run_one_function({
          "name": "my_tool",
          "arguments": {"input": "example_value"}
      })

   Parameters
   ----------

   - **input** (string, required): Input parameter description

Contributing Workflow
---------------------

1. Create a feature branch:

.. code-block:: bash

   git checkout -b feature/my-feature

2. Make your changes and commit:

.. code-block:: bash

   git add .
   git commit -m "feat: add my new tool

   - Implement MyTool class
   - Add comprehensive tests
   - Update documentation"

3. Push and create a pull request:

.. code-block:: bash

   git push origin feature/my-feature

Commit Types
~~~~~~~~~~~~

- ``feat``: New features
- ``fix``: Bug fixes
- ``docs``: Documentation updates
- ``test``: Test additions or modifications
- ``refactor``: Code refactoring
- ``style``: Code style changes
- ``chore``: Build/maintenance tasks

Review Process
--------------

All contributions go through:

1. **Automated Checks**: CI runs tests, linting, and type checking
2. **Manual Review**: Maintainers review code quality and design
3. **Documentation Review**: Ensure docs are clear and complete
4. **Testing**: Verify functionality works as expected

Troubleshooting Tool Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your tool is not being imported correctly, check these common issues:

**ImportError: cannot import name 'MyTool'**
- Verify you added the tool to all four locations in ``__init__.py``
- Check that the module name in the import statement matches your file name
- Ensure the class name matches exactly (case-sensitive)

**AttributeError: module 'tooluniverse' has no attribute 'MyTool'**
- Verify the tool name is added to the ``__all__`` list
- Check that the tool name in ``__all__`` matches the class name exactly
- Ensure you're importing from the correct module

**LazyImportProxy issues**
- Verify the module name in ``_LazyImportProxy("module_name", "ClassName")`` matches your file name
- Check that the class name in the proxy matches your actual class name
- Ensure the module is in the correct location (``src/tooluniverse/tools/``)

**Testing your integration**:

.. code-block:: python

   # Test 1: Direct import
   from tooluniverse import MyTool
   print(f"Tool class: {MyTool}")
   
   # Test 2: Check if it's in __all__
   from tooluniverse import __all__
   print(f"MyTool in __all__: {'MyTool' in __all__}")
   
   # Test 3: Instantiate the tool
   tool = MyTool()
   print(f"Tool instance: {tool}")

Getting Help
------------

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: shanghuagao@gmail.com

Types of Contributions
----------------------

Bug Reports
~~~~~~~~~~~

Include:
- Python version and OS
- ToolUniverse version
- Minimal code to reproduce
- Full error traceback
- Expected vs actual behavior

Feature Requests
~~~~~~~~~~~~~~~~

Provide:
- Clear use case description
- Proposed API design
- Implementation suggestions
- Impact on existing code

Documentation Improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~

Help by:
- Fixing typos and grammar
- Adding missing examples
- Clarifying confusing sections
- Translating to other languages

Thank you for contributing to ToolUniverse! 🧬🔬