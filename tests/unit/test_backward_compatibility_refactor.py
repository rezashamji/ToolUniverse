#!/usr/bin/env python3
"""
Backward compatibility tests for BaseTool refactoring.

This module ensures that existing code continues to work after the refactoring.
"""

import pytest
import warnings
from unittest.mock import Mock, patch
from tooluniverse import ToolUniverse
from tooluniverse.exceptions import (
    ToolError, ToolValidationError, ToolAuthError, ToolRateLimitError
)


@pytest.mark.unit
class TestBackwardCompatibility:
    """Test backward compatibility after BaseTool refactoring."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()

    def test_old_exception_classes_removed(self):
        """Test that old exception classes are no longer available."""
        # These should no longer be available
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import ToolExecutionError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import ValidationError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import AuthenticationError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import RateLimitError

    def test_new_exception_classes_work(self):
        """Test that new exception classes work without warnings."""
        # These should work without warnings
        ToolError("test message")
        ToolValidationError("test message")
        ToolAuthError("test message")
        ToolRateLimitError("test message")

    def test_tooluniverse_run_one_function_compatibility(self):
        """Test that ToolUniverse.run_one_function still works with old signature."""
        # Test with old signature (no new parameters)
        function_call = {
            "name": "nonexistent_tool",
            "arguments": {"param": "value"}
        }
        
        result = self.tu.run_one_function(function_call)
        
        # Should return error in old format
        assert isinstance(result, dict)
        assert "error" in result
        assert "Tool 'nonexistent_tool' not found" in result["error"]

    def test_tooluniverse_run_one_function_new_parameters(self):
        """Test that new parameters work with backward compatibility."""
        function_call = {
            "name": "nonexistent_tool",
            "arguments": {"param": "value"}
        }
        
        # Test with new parameters
        result = self.tu.run_one_function(
            function_call, 
            use_cache=True, 
            validate=True
        )
        
        # Should still return error in compatible format
        assert isinstance(result, dict)
        assert "error" in result

    def test_tooluniverse_error_format_compatibility(self):
        """Test that error format remains backward compatible."""
        function_call = {
            "name": "nonexistent_tool",
            "arguments": {"param": "value"}
        }
        
        result = self.tu.run_one_function(function_call)
        
        # Old format: simple error string
        assert "error" in result
        assert isinstance(result["error"], str)
        
        # New format: structured error details
        assert "error_details" in result
        assert isinstance(result["error_details"], dict)
        assert "type" in result["error_details"]
        assert "message" in result["error_details"]

    def test_tool_check_function_call_compatibility(self):
        """Test that tool.check_function_call still works."""
        from tooluniverse.base_tool import BaseTool
        
        tool_config = {
            "name": "test_tool",
            "parameter": {
                "type": "object",
                "properties": {
                    "param": {"type": "string", "required": True}
                }
            }
        }
        
        tool = BaseTool(tool_config)
        
        # Test valid function call
        valid_call = {
            "name": "test_tool",
            "arguments": {"param": "value"}
        }
        
        is_valid, message = tool.check_function_call(valid_call)
        assert is_valid is True
        assert "valid" in message.lower()  # Check for success message
        
        # Test invalid function call
        invalid_call = {
            "name": "test_tool",
            "arguments": {}  # Missing required param
        }
        
        is_valid, message = tool.check_function_call(invalid_call)
        assert is_valid is False
        assert "param" in message

    def test_tool_get_required_parameters_compatibility(self):
        """Test that tool.get_required_parameters still works."""
        from tooluniverse.base_tool import BaseTool
        
        tool_config = {
            "name": "test_tool",
            "parameter": {
                "type": "object",
                "properties": {
                    "required_param": {"type": "string"},
                    "optional_param": {"type": "string"}
                },
                "required": ["required_param"]
            }
        }
        
        tool = BaseTool(tool_config)
        required_params = tool.get_required_parameters()
        
        assert "required_param" in required_params
        assert "optional_param" not in required_params

    def test_tool_config_defaults_compatibility(self):
        """Test that tool config defaults loading still works."""
        from tooluniverse.base_tool import BaseTool
        
        # Test with minimal config
        tool_config = {"name": "minimal_tool"}
        tool = BaseTool(tool_config)
        
        # Should not crash
        assert tool.tool_config["name"] == "minimal_tool"

    def test_tooluniverse_fallback_logic(self):
        """Test that ToolUniverse fallback logic works for tools without new methods."""
        # Mock a tool without new methods
        class OldStyleTool:
            def __init__(self, tool_config):
                self.tool_config = tool_config
            
            def run(self, arguments=None):
                return "old_style_result"
        
        # Mock tool discovery and add to all_tool_dict
        with patch.object(self.tu, 'init_tool') as mock_init_tool:
            mock_init_tool.return_value = OldStyleTool({"name": "old_tool"})
            
            # Add tool to all_tool_dict so it can be found
            self.tu.all_tool_dict["old_tool"] = {
                "name": "old_tool",
                "parameter": {
                    "type": "object",
                    "properties": {}
                }
            }
            
            function_call = {
                "name": "old_tool",
                "arguments": {}
            }
            
            result = self.tu.run_one_function(function_call)
            
            # Should work with fallback logic
            assert result == "old_style_result"

    def test_deprecation_warnings_are_issued(self):
        """Test that old exception classes are no longer available (they were removed)."""
        # These should no longer be available since we removed them completely
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import ToolExecutionError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import ValidationError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import AuthenticationError
        with pytest.raises(ImportError):
            from tooluniverse.base_tool import RateLimitError

    def test_new_exception_classes_work_without_warnings(self):
        """Test that new exception classes work without deprecation warnings."""
        # Should not issue deprecation warnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            
            # These should not raise any warnings
            ToolError("test message")
            ToolValidationError("test message")
            ToolAuthError("test message")
            ToolRateLimitError("test message")

    def test_tooluniverse_caching_compatibility(self):
        """Test that caching works with both old and new tools."""
        function_call = {
            "name": "nonexistent_tool",
            "arguments": {"param": "value"}
        }
        
        # Test caching with non-existent tool (should not cache errors)
        result1 = self.tu.run_one_function(function_call, use_cache=True)
        result2 = self.tu.run_one_function(function_call, use_cache=True)
        
        # Both should return the same error
        assert result1["error"] == result2["error"]

    def test_tooluniverse_validation_compatibility(self):
        """Test that validation works with both old and new tools."""
        function_call = {
            "name": "nonexistent_tool",
            "arguments": {"param": "value"}
        }
        
        # Test validation with non-existent tool
        result = self.tu.run_one_function(function_call, validate=True)
        
        # Should return validation error
        assert "error" in result
        assert "not found" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__])
