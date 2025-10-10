#!/usr/bin/env python3
"""
Tool Finder Example

This example demonstrates how to use ToolUniverse's tool finding capabilities
to discover relevant tools based on descriptions or keywords.

The example shows:
1. How to use Tool_Finder for semantic tool discovery
2. How to use Tool_Finder_Keyword for keyword-based tool discovery
3. Error handling and timeout management

Requirements:
- ToolUniverse installed
- Valid API keys for LLM services (if using semantic search)
"""

from tooluniverse import ToolUniverse
import time


def main():
    """Main function demonstrating tool finder usage."""
    print("🔍 Tool Finder Example")
    print("=" * 50)
    
    # Initialize ToolUniverse
    print("Initializing ToolUniverse...")
    tooluni = ToolUniverse()
    tooluni.load_tools()
    print("✅ ToolUniverse initialized successfully")
    
    # Example queries demonstrating different tool finding methods
    test_queries = [
        {
            "name": "Tool_Finder",
            "arguments": {
                "description": "a tool for finding tools related to diseases",
                "limit": 5,  # Reduced limit to avoid timeout
                "return_call_result": False,
            },
        },
        {
            "name": "Tool_Finder_Keyword", 
            "arguments": {
                "description": "disease", 
                "limit": 3  # Reduced limit to avoid timeout
            }
        },
    ]
    
    # Run example queries with timeout handling
    print(f"\nRunning {len(test_queries)} example queries...")
    
    for idx, query in enumerate(test_queries, 1):
        print(f"\n[{idx}] Running tool: {query['name']}")
        print(f"Arguments: {query['arguments']}")
        
        try:
            start_time = time.time()
            result = tooluni.run(query)
            end_time = time.time()
            
            print(f"✅ Success! (took {end_time - start_time:.2f}s)")
            print("Result:")
            if isinstance(result, dict):
                print(f"Found {len(result.get('tools', []))} tools")
                for tool in result.get('tools', [])[:3]:  # Show first 3 tools
                    print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')[:100]}...")
            else:
                print(str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if "timeout" in str(e).lower():
                print("💡 Tip: This tool may require external API calls. Try reducing the 'limit' parameter.")
    
    print("\n🎉 Tool Finder Example completed!")


if __name__ == "__main__":
    main()
