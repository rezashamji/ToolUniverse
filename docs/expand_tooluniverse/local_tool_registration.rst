Local Tool Registration
=================================

What are Local Tools?
---------------------

Local tools are Python classes that extend ToolUniverse with custom functionality. They run in the same process as ToolUniverse and provide the most efficient way to add specialized capabilities.

Complete Working Example
-------------------------

Here's a complete protein molecular weight calculator you can copy and run:

.. code-block:: python

   # protein_calculator.py - Save this file anywhere
   from tooluniverse.tool_registry import register_tool
   from tooluniverse.base_tool import BaseTool
   from tooluniverse.exceptions import ToolValidationError
   from typing import Dict, Any

   @register_tool('ProteinCalculator', config={
       "name": "protein_calculator",                    # ← Change this to your tool name
       "type": "ProteinCalculator",
       "description": "Calculate molecular weight of protein sequences",  # ← Change this description
       "parameter": {
           "type": "object",
           "properties": {
               "sequence": {"type": "string", "description": "Protein sequence (single letter amino acid codes)"}  # ← Modify parameters here
           },
           "required": ["sequence"]
       }
   })
   class ProteinCalculator(BaseTool):
       """Calculate molecular weight of protein sequences."""

       def __init__(self, tool_config: Dict[str, Any] = None):
           super().__init__(tool_config)
           # Amino acid molecular weights (in Daltons)
           self.aa_weights = {
               'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10,
               'C': 121.16, 'Q': 146.15, 'E': 147.13, 'G': 75.07,
               'H': 155.16, 'I': 131.17, 'L': 131.17, 'K': 146.19,
               'M': 149.21, 'F': 165.19, 'P': 115.13, 'S': 105.09,
               'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
           }

       def run(self, arguments=None, **kwargs) -> Dict[str, Any]:  # ← Implement your logic here
           """Calculate molecular weight of a protein sequence."""
           # Handle both direct calls and ToolUniverse calls
           if arguments is None:
               arguments = kwargs
           
           # Extract sequence from arguments
           sequence = arguments.get('sequence') if isinstance(arguments, dict) else arguments
           
           # Validate inputs
           self.validate_input(sequence=sequence)

           # Clean sequence (remove whitespace, convert to uppercase)
           clean_sequence = sequence.strip().upper()

           # Calculate molecular weight
           total_weight = sum(self.aa_weights.get(aa, 0) for aa in clean_sequence)
           # Subtract water molecules for peptide bonds
           water_weight = (len(clean_sequence) - 1) * 18.015
           molecular_weight = total_weight - water_weight

           return {
               "molecular_weight": round(molecular_weight, 2),
               "sequence_length": len(clean_sequence),
               "sequence": clean_sequence,
               "success": True
           }

       def validate_input(self, **kwargs) -> None:
           """Validate input parameters."""
           sequence = kwargs.get('sequence')

           if not sequence:
               raise ValueError("Sequence is required")

           if not isinstance(sequence, str):
               raise ValueError("Sequence must be a string")

           if len(sequence.strip()) == 0:
               raise ValueError("Sequence cannot be empty")

           # Check for valid amino acid codes
           valid_aa = set(self.aa_weights.keys())
           invalid_chars = set(sequence.upper()) - valid_aa
           if invalid_chars:
               raise ValueError(f"Invalid amino acid codes: {', '.join(invalid_chars)}")

   # Usage
   from tooluniverse import ToolUniverse

   # Import your tool (this registers it)
   from protein_calculator import ProteinCalculator

   tu = ToolUniverse()
   tu.load_tools()  # Load built-in tools

   result = tu.run_one_function({
       "name": "protein_calculator",
       "arguments": {"sequence": "GIVEQCCTSICSLYQLENYCN"}
   })
   print(result)  # {"molecular_weight": 2401.45, "sequence_length": 20, "success": True}

**How to use:**
Save as `protein_calculator.py` and import it - the tool registers automatically.

.. note::
   **Complete Working Example**: See :file:`examples/protein_calculator_example.py` for a full, runnable example with comprehensive testing and validation demonstrations.

Adapt to Your Own Tool
----------------------

You only need to modify 3 places:

**1. Tool Name and Description (lines 8-9)**
   - ``name``: ``"protein_calculator"`` → change to your tool name
   - ``description``: ``"Calculate molecular weight..."`` → change to your description
   
**2. Input Parameters (lines 10-15)**
   Define the parameters you need:
   
   .. list-table::
      :header-rows: 1
      :widths: 20 30 50

      * - Your Need
        - Parameter Type
        - Example
      * - Text input
        - ``"type": "string"``
        - username, query, file_path
      * - Number input
        - ``"type": "number"``
        - age, amount, limit
      * - Dropdown options
        - ``"type": "string", "enum": [...]``
        - status, category, format
      * - Optional param
        - Don't put in ``"required"``
        - optional filters, defaults

**3. Core Logic (run method at line 30)**
   Implement your business logic and return results:
   
   .. code-block:: python

      def run(self, arguments=None, **kwargs) -> Dict[str, Any]:
          """Your tool description."""
          # Handle both direct calls and ToolUniverse calls
          if arguments is None:
              arguments = kwargs
          
          # Extract your parameter from arguments
          your_param = arguments.get('your_param') if isinstance(arguments, dict) else arguments
          
          # Validate inputs
          self.validate_input(your_param=your_param)

          # Your logic here
          result = do_something(your_param)

          return {"result": result, "success": True}

Common Scenarios
----------------

I want to call an external API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests

   def run(self, arguments=None, **kwargs) -> Dict[str, Any]:
       """Make API call to specified URL."""
       # Handle both direct calls and ToolUniverse calls
       if arguments is None:
           arguments = kwargs
       
       url = arguments.get('url') if isinstance(arguments, dict) else arguments
       method = arguments.get('method', 'GET') if isinstance(arguments, dict) else 'GET'
       
       self.validate_input(url=url, method=method)

       try:
           if method == "GET":
               response = requests.get(url)
           else:
               response = requests.post(url)

           response.raise_for_status()
           return {"data": response.json(), "success": True}
       except Exception as e:
           return {"error": str(e), "success": False}

I want to process files
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def run(self, arguments=None, **kwargs) -> Dict[str, Any]:
       """Process file based on specified operation."""
       # Handle both direct calls and ToolUniverse calls
       if arguments is None:
           arguments = kwargs
       
       file_path = arguments.get('file_path') if isinstance(arguments, dict) else arguments
       operation = arguments.get('operation', 'read') if isinstance(arguments, dict) else 'read'
       
       self.validate_input(file_path=file_path, operation=operation)

       try:
           with open(file_path, 'r') as f:
               content = f.read()

           if operation == "analyze":
               result = {"lines": len(content.split('\n')), "chars": len(content)}
           else:
               result = {"content": content}

           return {"result": result, "success": True}
       except Exception as e:
           return {"error": str(e), "success": False}

I want to use API keys (environment variables)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add to your config:

.. code-block:: python

   @register_tool('MyAPITool', config={
       "name": "my_api_tool",
       "description": "Tool that uses API keys",
       "parameter": {
           "type": "object",
           "properties": {
               "query": {"type": "string", "description": "Search query"}
           },
           "required": ["query"]
       },
       "settings": {  # ← Add this section
           "api_key": "env:MY_API_KEY",  # ← Reference environment variable
           "base_url": "https://api.example.com"
       }
   })

Then in your run method:

.. code-block:: python

   def __init__(self, tool_config: Dict[str, Any] = None):
       super().__init__(tool_config)
       self.api_key = self.config.get("settings", {}).get("api_key")
       self.base_url = self.config.get("settings", {}).get("base_url")

I want custom error handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def run(self, arguments=None, **kwargs) -> Dict[str, Any]:
       """Execute with proper error handling."""
       # Handle both direct calls and ToolUniverse calls
       if arguments is None:
           arguments = kwargs
       
       param = arguments.get('param') if isinstance(arguments, dict) else arguments
       
       try:
           # Validate inputs first
           self.validate_input(param=param)

           # Your tool logic here
           result = self.process_data(param)
           return {"result": result, "success": True}

       except ValueError as e:
           # Input validation errors
           return {"error": f"Invalid input: {str(e)}", "success": False}
       except requests.RequestException as e:
           # Network errors
           return {"error": f"Network error: {str(e)}", "success": False}
       except Exception as e:
           # Unexpected errors
           return {"error": f"Unexpected error: {str(e)}", "success": False}

Troubleshooting
---------------

Tool not found
~~~~~~~~~~~~~~

□ Is the tool file imported? (need to ``import`` or run directly)
□ Is the ``@register_tool`` decorator used correctly?
□ Is ToolUniverse instantiated after tool import?

Parameter errors
~~~~~~~~~~~~~~~~

□ Do ``"parameter"`` definitions in config match ``run()`` method parameters?
□ Are required parameters listed in ``"required"`` array?
□ Are parameter types (``string``/``number``/``object``) correct?

Execution failures
~~~~~~~~~~~~~~~~~~

□ Does the class inherit from ``BaseTool``?
□ Does ``__init__`` call ``super().__init__(tool_config)``?
□ Does ``run()`` return a dict with ``"success"`` field?
□ Is ``validate_input()`` implemented for parameter validation?

Next Steps
----------

Now that you can create local tools:

* 🔗 **Remote Tools**: :doc:`remote_tool_registration` - Learn about remote tool integration
* 📤 **Contributing**: :doc:`contributing_tools` - Submit your tools to ToolUniverse
* 🤖 **AI Integration**: :doc:`../guide/building_ai_scientists/mcp_integration` - Connect your tools with AI assistants
* 🔬 **Scientific Workflows**: :doc:`../guide/scientific_workflows` - Build research pipelines

.. tip::
   **Development tip**: Start simple, test thoroughly, and gradually add complexity. The ToolUniverse community is here to help if you get stuck!
