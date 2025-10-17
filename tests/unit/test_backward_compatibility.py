#!/usr/bin/env python3
"""
Backward Compatibility Tests for ToolUniverse

Tests that existing APIs continue to work unchanged after enhancements.
"""

import sys
import unittest
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tooluniverse import ToolUniverse


@pytest.mark.unit
class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility of existing APIs."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()
    
    def test_run_one_function_signature(self):
        """Test that run_one_function signature is backward compatible."""
        # Test original signature still works
        result = self.tu.run_one_function({
            "name": "UniProt_get_entry_by_accession",
            "arguments": {"accession": "P05067"}
        })
        
        # Should return a result (may be error if tool not available)
        self.assertIsNotNone(result)
    
    def test_run_one_function_with_stream_callback(self):
        """Test that stream_callback parameter still works."""
        callback_called = False
        
        def test_callback(chunk):
            nonlocal callback_called
            callback_called = True
        
        result = self.tu.run_one_function(
            {"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "P05067"}},
            stream_callback=test_callback
        )
        
        # Callback may or may not be called depending on tool implementation
        self.assertIsNotNone(result)
    
    def test_error_format_backward_compatibility(self):
        """Test that error format includes backward-compatible 'error' field."""
        # Test with non-existent tool
        result = self.tu.run_one_function({
            "name": "NonExistentTool",
            "arguments": {}
        })
        
        # Should return error in dual format
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIsInstance(result["error"], str)
        
        # Should also include new structured format
        self.assertIn("error_details", result)
        self.assertIsInstance(result["error_details"], dict)
        self.assertIn("type", result["error_details"])
    
    def test_smcp_server_initialization(self):
        """Test that SMCP server can still be initialized."""
        try:
            from tooluniverse import SMCP
            server = SMCP()
            self.assertIsNotNone(server)
            self.assertIsNotNone(server.tooluniverse)
        except ImportError:
            # SMCP not available, skip test
            self.skipTest("SMCP not available")
    
    def test_direct_tool_class_usage(self):
        """Test that direct tool class usage still works."""
        try:
            from tooluniverse import UniProtRESTTool
            
            # Create tool instance directly with required fields
            tool_config = {
                "name": "test_tool",
                "type": "UniProtRESTTool",
                "fields": {
                    "endpoint": "test_endpoint"
                },
                "parameter": {
                    "type": "object",
                    "properties": {
                        "accession": {"type": "string"}
                    },
                    "required": ["accession"]
                }
            }
            
            tool = UniProtRESTTool(tool_config)
            self.assertIsNotNone(tool)
            
        except ImportError:
            # Tool class not available, skip test
            self.skipTest("UniProtRESTTool not available")
    
    def test_new_parameters_have_defaults(self):
        """Test that new parameters have sensible defaults."""
        # Test use_cache parameter
        result1 = self.tu.run_one_function({
            "name": "UniProt_get_entry_by_accession",
            "arguments": {"accession": "P05067"}
        })
        
        result2 = self.tu.run_one_function({
            "name": "UniProt_get_entry_by_accession",
            "arguments": {"accession": "P05067"}
        }, use_cache=False)
        
        # Results should be the same (both with cache disabled)
        self.assertEqual(type(result1), type(result2))
        
        # Test validate parameter
        result3 = self.tu.run_one_function({
            "name": "UniProt_get_entry_by_accession",
            "arguments": {"accession": "P05067"}
        }, validate=True)
        
        # Should work with validation enabled
        self.assertIsNotNone(result3)
    
    def test_dynamic_tools_namespace(self):
        """Test that new dynamic tools namespace works."""
        # Test that tools attribute exists
        self.assertTrue(hasattr(self.tu, 'tools'))
        
        # Test that it's a ToolNamespace
        from tooluniverse.execute_function import ToolNamespace
        self.assertIsInstance(self.tu.tools, ToolNamespace)
        
        # Test that we can access a tool
        try:
            tool_callable = self.tu.tools.UniProt_get_entry_by_accession
            self.assertIsNotNone(tool_callable)
        except AttributeError:
            # Tool not available, that's okay
            pass
    
    def test_lifecycle_methods_exist(self):
        """Test that new lifecycle methods exist."""
        # Test that new methods exist
        self.assertTrue(hasattr(self.tu, 'refresh_tools'))
        self.assertTrue(hasattr(self.tu, 'eager_load_tools'))
        self.assertTrue(hasattr(self.tu, 'clear_cache'))
        
        # Test that they can be called
        self.tu.refresh_tools()
        self.tu.eager_load_tools([])
        self.tu.clear_cache()
    
    def test_cache_functionality(self):
        """Test that caching functionality works."""
        # Test cache operations
        self.tu.clear_cache()
        
        # Test that cache is empty initially
        self.assertEqual(len(self.tu._cache), 0)
        
        # Test caching a result
        try:
            result1 = self.tu.run_one_function({
                "name": "UniProt_get_entry_by_accession",
                "arguments": {"accession": "P05067"}
            }, use_cache=True)
            
            # Cache should have one entry if successful
            if result1 is not None:
                self.assertEqual(len(self.tu._cache), 1)
                
                # Test cache hit
                result2 = self.tu.run_one_function({
                    "name": "UniProt_get_entry_by_accession",
                    "arguments": {"accession": "P05067"}
                }, use_cache=True)
                
                # Results should be the same
                self.assertEqual(result1, result2)
            else:
                # If tool execution failed, cache should still be empty
                self.assertEqual(len(self.tu._cache), 0)
                
        except Exception:
            # If tool execution fails, cache should still be empty
            self.assertEqual(len(self.tu._cache), 0)
        
        # Clear cache
        self.tu.clear_cache()
        self.assertEqual(len(self.tu._cache), 0)


class TestErrorHandlingCompatibility(unittest.TestCase):
    """Test error handling backward compatibility."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()
    
    def test_validation_error_format(self):
        """Test validation error format."""
        # Test with invalid parameters
        result = self.tu.run_one_function({
            "name": "UniProt_get_entry_by_accession",
            "arguments": {"invalid_param": "test"}
        }, validate=True)
        
        # Should return dual-format error
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("error_details", result)
        
        # Error details should be structured
        error_details = result["error_details"]
        self.assertIn("type", error_details)
        self.assertIn("message", error_details)
        self.assertIn("retriable", error_details)
        self.assertIn("next_steps", error_details)
    
    def test_tool_not_found_error(self):
        """Test tool not found error format."""
        result = self.tu.run_one_function({
            "name": "NonExistentTool",
            "arguments": {}
        })
        
        # Should return dual-format error
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("error_details", result)
        
        # Error should indicate tool not found
        self.assertIn("not found", result["error"].lower())
        self.assertEqual(result["error_details"]["type"], "ToolUnavailableError")


if __name__ == "__main__":
    unittest.main()
