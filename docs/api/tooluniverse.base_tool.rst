tooluniverse.base_tool module
==============================

.. currentmodule:: tooluniverse.base_tool

The BaseTool class provides the foundation for all ToolUniverse tools with enhanced capabilities for validation, error handling, and caching.

Base Tool Class
~~~~~~~~~~~~~~~

.. autoclass:: BaseTool
   :members:
   :special-members: __init__
   :show-inheritance:

   The base class for all ToolUniverse tools. Provides standard capabilities that can be
   overridden by custom tool implementations.

   **New Capabilities (v1.1+):**
   
   - :meth:`validate_parameters` - Parameter validation with schema support
   - :meth:`handle_error` - Structured error classification
   - :meth:`get_cache_key` - Custom cache key generation
   - :meth:`supports_streaming` - Declare streaming support
   - :meth:`supports_caching` - Declare caching support
   - :meth:`get_tool_info` - Comprehensive tool metadata

   **Example:**
   
   .. code-block:: python

      from tooluniverse.base_tool import BaseTool
      from tooluniverse.exceptions import ToolValidationError
      
      class MyCustomTool(BaseTool):
          def validate_parameters(self, arguments):
              # Custom validation logic
              if "required_field" not in arguments:
                  return ToolValidationError(
                      "Missing required field",
                      next_steps=["Add required_field parameter"]
                  )
              return super().validate_parameters(arguments)
          
          def run(self, arguments=None):
              return "Custom tool result"

For more information about the exception system, see :mod:`tooluniverse.exceptions`.
