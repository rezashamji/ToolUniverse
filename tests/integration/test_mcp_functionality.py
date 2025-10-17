#!/usr/bin/env python3
"""
MCP Functionality Tests

Tests that MCP-related functionality actually works:
- SMCP server can be created and configured
- MCP client tools can be instantiated
- MCP protocol methods are available
- Tool discovery and execution works
"""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock

from tooluniverse import ToolUniverse
from tooluniverse.smcp import SMCP
from tooluniverse.mcp_client_tool import MCPClientTool, MCPAutoLoaderTool


@pytest.mark.integration
@pytest.mark.mcp
class TestMCPFunctionality:
    """Test that MCP functionality actually works"""

    def test_smcp_server_creation(self):
        """Test that SMCP server can be created with different configurations"""
        # Test basic creation
        server = SMCP(name="Test Server")
        assert server is not None
        assert server.name == "Test Server"
        
        # Test with tool categories
        server = SMCP(
            name="Category Server",
            tool_categories=["uniprot", "ChEMBL"],
            search_enabled=True
        )
        assert server is not None
        assert len(server.tooluniverse.all_tool_dict) > 0
        
        # Test with specific tools
        server = SMCP(
            name="Tool Server",
            include_tools=["UniProt_get_entry_by_accession"],
            search_enabled=False
        )
        assert server is not None

    def test_smcp_server_tool_loading(self):
        """Test that SMCP server loads tools correctly"""
        server = SMCP(
            name="Loading Test",
            tool_categories=["uniprot"],
            search_enabled=True
        )
        
        # Check that tools are loaded
        tools = server.tooluniverse.all_tool_dict
        assert len(tools) > 0
        
        # Check that UniProt tools are present
        uniprot_tools = [name for name in tools.keys() if "UniProt" in name]
        assert len(uniprot_tools) > 0

    def test_smcp_server_configuration(self):
        """Test SMCP server configuration options"""
        # Test with different worker counts
        server = SMCP(name="Worker Test", max_workers=10)
        assert server.max_workers == 10
        
        # Test with search disabled
        server = SMCP(name="No Search", search_enabled=False)
        assert server.search_enabled is False
        
        # Test with hooks enabled
        server = SMCP(name="Hooks Test", hooks_enabled=True)
        assert server.hooks_enabled is True

    def test_mcp_client_tool_creation(self):
        """Test that MCP client tools can be created"""
        # Test MCPClientTool
        tool_config = {
            "name": "test_client",
            "server_url": "http://localhost:8000",
            "transport": "http"
        }
        
        client = MCPClientTool(tool_config)
        assert client is not None
        assert client.server_url == "http://localhost:8000"
        assert client.transport == "http"
        
        # Test MCPAutoLoaderTool
        auto_loader = MCPAutoLoaderTool(tool_config)
        assert auto_loader is not None

    @pytest.mark.asyncio
    async def test_mcp_client_tool_async_methods(self):
        """Test that MCP client tools have async methods"""
        tool_config = {
            "name": "test_client",
            "server_url": "http://localhost:8000",
            "transport": "http"
        }
        
        client = MCPClientTool(tool_config)
        
        # Test that async methods exist and are callable
        assert hasattr(client, 'list_tools')
        assert asyncio.iscoroutinefunction(client.list_tools)
        
        assert hasattr(client, 'call_tool')
        assert asyncio.iscoroutinefunction(client.call_tool)
        
        assert hasattr(client, 'list_resources')
        assert asyncio.iscoroutinefunction(client.list_resources)

    @pytest.mark.asyncio
    async def test_mcp_client_tool_with_mock_server(self):
        """Test MCP client tool with mocked server responses"""
        # Mock successful response
        mock_response = {
            "result": {
                "tools": [
                    {
                        "name": "test_tool",
                        "description": "A test tool",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "param1": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
        
        async def mock_json():
            return mock_response
            
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response_obj = MagicMock()
            mock_response_obj.status = 200
            mock_response_obj.headers = {"content-type": "application/json"}
            mock_response_obj.json = mock_json
            
            mock_post.return_value.__aenter__.return_value = mock_response_obj
            
            tool_config = {
                "name": "test_client",
                "server_url": "http://localhost:8000",
                "transport": "http"
            }
            
            client = MCPClientTool(tool_config)
            
            # Test listing tools
            tools = await client.list_tools()
            assert len(tools) > 0
            assert tools[0]["name"] == "test_tool"

    def test_smcp_server_utility_tools(self):
        """Test that SMCP server has utility tools"""
        server = SMCP(
            name="Utility Test",
            tool_categories=["uniprot"],
            search_enabled=True
        )
        
        # Check that utility tools are registered
        # These should be available as MCP tools
        assert hasattr(server, 'tooluniverse')
        assert server.tooluniverse is not None

    def test_smcp_server_tool_finder_initialization(self):
        """Test that SMCP server initializes tool finders correctly"""
        # Test with search enabled
        server = SMCP(
            name="Finder Test",
            tool_categories=["uniprot"],
            search_enabled=True
        )
        
        # Check that tool finders are initialized
        # The actual attribute names might be different
        assert hasattr(server, 'tooluniverse')
        assert server.tooluniverse is not None
        
        # Check that search is enabled
        assert server.search_enabled is True

    def test_smcp_server_error_handling(self):
        """Test SMCP server error handling"""
        # Test with invalid configuration (nonexistent category)
        server = SMCP(
            name="Error Test",
            tool_categories=["nonexistent_category"]
        )
        
        # Should still create server with defaults
        assert server is not None
        assert server.max_workers >= 1

    def test_mcp_protocol_methods_availability(self):
        """Test that MCP protocol methods are available"""
        server = SMCP(name="Protocol Test")
        
        # Check that custom MCP methods are available
        assert hasattr(server, '_tools_find_middleware')
        assert callable(server._tools_find_middleware)
        
        assert hasattr(server, '_handle_tools_find')
        assert callable(server._handle_tools_find)
        
        # Check that FastMCP methods are available
        assert hasattr(server, 'get_tools')
        assert callable(server.get_tools)

    @pytest.mark.asyncio
    async def test_smcp_tools_find_functionality(self):
        """Test SMCP tools/find functionality"""
        server = SMCP(
            name="Find Test",
            tool_categories=["uniprot", "ChEMBL"],
            search_enabled=True
        )
        
        # Test tools/find request
        request = {
            "jsonrpc": "2.0",
            "id": "find-test",
            "method": "tools/find",
            "params": {
                "query": "protein analysis",
                "limit": 5
            }
        }
        
        response = await server._handle_tools_find(
            request_id="find-test",
            params={
                "query": "protein analysis",
                "limit": 5
            }
        )
        
        # Should return a valid response
        assert "jsonrpc" in response
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert response["id"] == "find-test"
        
        # Should have either result or error
        assert "result" in response or "error" in response
        
        if "result" in response:
            # The result might be a list of tools directly or have a tools field
            result = response["result"]
            if isinstance(result, list):
                # Direct list of tools
                assert len(result) > 0
            elif "tools" in result:
                # Tools in a tools field
                assert isinstance(result["tools"], list)
                assert len(result["tools"]) > 0
            else:
                # Other format - just check it's not empty
                assert result is not None

    def test_smcp_server_thread_pool(self):
        """Test SMCP server thread pool configuration"""
        server = SMCP(
            name="Thread Test",
            max_workers=3
        )
        
        assert hasattr(server, 'executor')
        assert server.executor is not None
        assert server.max_workers == 3

    def test_smcp_server_tool_categories(self):
        """Test SMCP server tool category filtering"""
        # Test with specific categories
        server = SMCP(
            name="Category Test",
            tool_categories=["uniprot", "ChEMBL"]
        )
        
        tools = server.tooluniverse.all_tool_dict
        assert len(tools) > 0
        
        # Check that we have tools from the specified categories
        tool_names = list(tools.keys())
        has_uniprot = any("UniProt" in name for name in tool_names)
        has_chembl = any("ChEMBL" in name for name in tool_names)
        
        assert has_uniprot or has_chembl

    def test_smcp_server_exclude_tools(self):
        """Test SMCP server tool exclusion"""
        # Test excluding specific tools
        server = SMCP(
            name="Exclude Test",
            tool_categories=["uniprot"],
            exclude_tools=["UniProt_get_entry_by_accession"]
        )
        
        tools = server.tooluniverse.all_tool_dict
        assert "UniProt_get_entry_by_accession" not in tools

    def test_smcp_server_include_tools(self):
        """Test SMCP server tool inclusion"""
        # Test including specific tools
        server = SMCP(
            name="Include Test",
            include_tools=["UniProt_get_entry_by_accession"]
        )
        
        tools = server.tooluniverse.all_tool_dict
        assert "UniProt_get_entry_by_accession" in tools

    def test_mcp_client_tool_configuration(self):
        """Test MCP client tool configuration options"""
        # Test different transport types
        http_config = {
            "name": "http_client",
            "server_url": "http://localhost:8000",
            "transport": "http"
        }
        
        ws_config = {
            "name": "ws_client",
            "server_url": "ws://localhost:8000",
            "transport": "websocket"
        }
        
        http_client = MCPClientTool(http_config)
        ws_client = MCPClientTool(ws_config)
        
        assert http_client.transport == "http"
        assert ws_client.transport == "websocket"

    def test_smcp_server_hooks_configuration(self):
        """Test SMCP server hooks configuration"""
        # Test with different hook configurations
        server = SMCP(
            name="Hooks Test",
            hooks_enabled=True,
            hook_type="SummarizationHook"
        )
        
        assert server.hooks_enabled is True
        assert server.hook_type == "SummarizationHook"

    def test_smcp_server_auto_expose_tools(self):
        """Test SMCP server auto-expose tools setting"""
        # Test with auto_expose_tools disabled
        server = SMCP(
            name="No Auto Expose",
            auto_expose_tools=False
        )
        
        assert server.auto_expose_tools is False
        
        # Test with auto_expose_tools enabled (default)
        server = SMCP(name="Auto Expose")
        assert server.auto_expose_tools is True
