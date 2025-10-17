Advanced Tool Development
==========================

This guide explains how to develop custom tools using the enhanced BaseTool capabilities. This is for advanced users who want to leverage the full power of ToolUniverse's tool development framework.

.. note::
   **New to tool development?** Start with :doc:`local_tool_registration` for basic tool creation, then return here for advanced features.

Overview
--------

The BaseTool class now provides several standard capabilities that can be overridden by custom tool implementations:

- **Parameter Validation**: `validate_parameters()` - Validate input parameters against schemas
- **Error Handling**: `handle_error()` - Classify exceptions into structured errors
- **Caching**: `get_cache_key()` - Generate cache keys for tool calls
- **Capability Queries**: `supports_streaming()`, `supports_caching()` - Declare tool capabilities
- **Tool Information**: `get_tool_info()` - Provide comprehensive tool metadata

Basic Tool Implementation
-------------------------

Here's a minimal tool implementation:

.. code-block:: python

    from tooluniverse.base_tool import BaseTool

    class MyTool(BaseTool):
        def run(self, arguments=None):
            # Your tool logic here
            return "tool_result"

Custom Parameter Validation
---------------------------

Override `validate_parameters()` to implement custom validation logic:

.. code-block:: python

    class GraphQLTool(BaseTool):
        def validate_parameters(self, arguments):
            # First, run base validation
            base_error = super().validate_parameters(arguments)
            if base_error:
                return base_error
            
            # Add custom validation
            query = arguments.get("query", "")
            if "mutation" in query.lower() and not self.allow_mutations:
                return ToolValidationError(
                    "Mutations not allowed",
                    details={"custom_rule": "no_mutations"}
                )
            
            return None  # Validation passed

Custom Error Handling
---------------------

Override `handle_error()` to provide tool-specific error classification:

.. code-block:: python

    class APITool(BaseTool):
        def handle_error(self, exception):
            error_str = str(exception).lower()
            
            # Tool-specific error patterns
            if "api_key" in error_str:
                return ToolAuthError(
                    "API key error",
                    next_steps=["Check API key", "Regenerate key if needed"]
                )
            
            # Fall back to base error handling
            return super().handle_error(exception)

Custom Caching
--------------

Override `get_cache_key()` for custom cache key generation:

.. code-block:: python

    class DatabaseTool(BaseTool):
        def get_cache_key(self, arguments):
            # Include database-specific information
            cache_data = {
                "tool_name": self.tool_config.get("name"),
                "query": arguments.get("query", ""),
                "database": self.tool_config.get("database", "default")
            }
            return f"db_{hash(json.dumps(cache_data, sort_keys=True))}"

Capability Declaration
----------------------

Override capability methods to declare tool features:

.. code-block:: python

    class StreamingTool(BaseTool):
        def supports_streaming(self):
            return True  # This tool supports streaming
        
        def supports_caching(self):
            # Don't cache streaming tools
            return False

Complete Example
----------------

Here's a complete example of a custom tool with all capabilities:

.. code-block:: python

    import json
    from tooluniverse.base_tool import BaseTool
    from tooluniverse.exceptions import ToolValidationError, ToolAuthError

    class WeatherTool(BaseTool):
        def __init__(self, tool_config):
            super().__init__(tool_config)
            self.api_key = tool_config.get("api_key")
            self.max_forecast_days = tool_config.get("max_forecast_days", 7)
        
        def validate_parameters(self, arguments):
            # Base validation
            base_error = super().validate_parameters(arguments)
            if base_error:
                return base_error
            
            # Weather-specific validation
            location = arguments.get("location", "")
            if not location:
                return ToolValidationError(
                    "Location is required",
                    details={"weather_rule": "location_required"}
                )
            
            days = arguments.get("days", 1)
            if days > self.max_forecast_days:
                return ToolValidationError(
                    f"Forecast days ({days}) exceeds maximum ({self.max_forecast_days})",
                    details={
                        "weather_rule": "max_days_exceeded",
                        "max_days": self.max_forecast_days
                    }
                )
            
            return None
        
        def handle_error(self, exception):
            error_str = str(exception).lower()
            
            if "api key" in error_str or "unauthorized" in error_str:
                return ToolAuthError(
                    "Weather API authentication failed",
                    next_steps=[
                        "Check API key configuration",
                        "Verify API key permissions",
                        "Contact API provider if issues persist"
                    ]
                )
            
            return super().handle_error(exception)
        
        def get_cache_key(self, arguments):
            # Include location and days in cache key
            cache_data = {
                "tool_name": "weather_tool",
                "location": arguments.get("location", ""),
                "days": arguments.get("days", 1)
            }
            return f"weather_{hash(json.dumps(cache_data, sort_keys=True))}"
        
        def supports_streaming(self):
            return False  # Weather data doesn't need streaming
        
        def supports_caching(self):
            return True  # Weather data can be cached
        
        def run(self, arguments=None):
            if arguments is None:
                arguments = {}
            
            location = arguments.get("location", "")
            days = arguments.get("days", 1)
            
            # Mock weather API call
            return {
                "location": location,
                "forecast": [
                    {"day": i+1, "temperature": 20+i, "condition": "sunny"}
                    for i in range(days)
                ],
                "source": "weather_api"
            }

Migration Guide
---------------

If you have existing tools, here's how to migrate them to use the new capabilities:

1. **No Changes Required**: Existing tools will continue to work without modification. The new methods have sensible defaults.

2. **Gradual Enhancement**: You can gradually add custom validation and error handling:

   .. code-block:: python

       # Before: Basic tool
       class MyTool(BaseTool):
           def run(self, arguments=None):
               return "result"
       
       # After: Enhanced tool
       class MyTool(BaseTool):
           def validate_parameters(self, arguments):
               # Add custom validation
               return super().validate_parameters(arguments)
           
           def handle_error(self, exception):
               # Add custom error handling
               return super().handle_error(exception)
           
           def run(self, arguments=None):
               return "result"

3. **Exception Handling**: If you're catching old exception classes, consider migrating to new ones:

   .. code-block:: python

       # Old way (still works)
       try:
           # tool operation
       except ValidationError as e:
           # handle error
       
       # New way (recommended)
       try:
           # tool operation
       except ToolValidationError as e:
           # handle error with structured details
           print(e.next_steps)

Best Practices
--------------

1. **Always Call Super**: When overriding methods, call the parent implementation first:

   .. code-block:: python

       def validate_parameters(self, arguments):
           # Run base validation first
           base_error = super().validate_parameters(arguments)
           if base_error:
               return base_error
           
           # Add custom validation
           # ...

2. **Provide Recovery Steps**: Include helpful next steps in error messages:

   .. code-block:: python

       return ToolValidationError(
           "Invalid input",
           next_steps=[
               "Check parameter format",
               "Review documentation",
               "Try with different values"
           ]
       )

3. **Use Structured Details**: Include structured information in error details:

   .. code-block:: python

       return ToolValidationError(
           "Validation failed",
           details={
               "field": "email",
               "expected_format": "user@domain.com",
               "provided_value": "invalid-email"
           }
       )

4. **Cache Appropriately**: Only cache results that are safe to cache:

   .. code-block:: python

       def supports_caching(self):
           # Don't cache if results change frequently
           return not self.tool_config.get("real_time", False)

Testing Custom Tools
--------------------

Test your custom tools using the standard testing patterns:

.. code-block:: python

    import pytest
    from tooluniverse.exceptions import ToolValidationError

    def test_custom_validation():
        tool = MyCustomTool(tool_config)
        
        # Test valid input
        error = tool.validate_parameters({"param": "value"})
        assert error is None
        
        # Test invalid input
        error = tool.validate_parameters({"param": "invalid"})
        assert isinstance(error, ToolValidationError)
        assert "param" in str(error)

Backward Compatibility
----------------------

All existing tools and code will continue to work without modification:

- Old exception classes still work (with deprecation warnings)
- Tools without new methods use default implementations
- ToolUniverse provides fallback logic for missing methods
- All existing APIs remain unchanged

The refactoring is designed to be completely backward compatible while providing enhanced capabilities for new development.
