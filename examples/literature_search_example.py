#!/usr/bin/env python3
"""
Literature Search Tools Example

This example demonstrates how to use literature search tools
available in ToolUniverse for finding academic papers and preprints.

The example shows:
1. How to search ArXiv preprints
2. How to search PubMed articles
3. How to search EuropePMC articles
4. Error handling and timeout management

Requirements:
- ToolUniverse installed
- Valid API keys for external services (if required)
"""

from tooluniverse import ToolUniverse
import time


def literature_search_examples():
    """Demonstrate literature search tools with timeout handling."""

    # Initialize ToolUniverse
    tu = ToolUniverse()
    tu.load_tools()

    print("🔍 Literature Search Tools Example")
    print("=" * 50)

    # Define a subset of literature search tools with simplified examples
    tools = [
        {
            "name": "ArXiv_search_papers",
            "description": "ArXiv preprints",
            "examples": [
                {"query": "machine learning", "limit": 2, "sort_by": "relevance"},
            ]
        },
        {
            "name": "PubMed_search_articles",
            "description": "PubMed articles",
            "examples": [
                {"query": "cancer immunotherapy", "limit": 2, "sort_by": "relevance"},
            ]
        },
        {
            "name": "EuropePMC_search_articles",
            "description": "EuropePMC articles",
            "examples": [
                {"query": "COVID-19 vaccine", "limit": 2},
            ]
        },
    ]

    print(f"Testing {len(tools)} literature search tools...")

    for tool_info in tools:
        tool_name = tool_info["name"]
        description = tool_info["description"]
        
        print(f"\n📚 Testing {tool_name} ({description})")
        
        for example in tool_info["examples"]:
            print(f"  Query: {example}")
            
            try:
                start_time = time.time()
                result = tu.run({
                    "name": tool_name,
                    "arguments": example
                })
                end_time = time.time()
                
                print(f"  ✅ Success! (took {end_time - start_time:.2f}s)")
                
                # Show a brief summary of results
                if isinstance(result, dict):
                    if 'articles' in result:
                        articles = result['articles']
                        print(f"  📄 Found {len(articles)} articles")
                        if articles:
                            first_article = articles[0]
                            title = first_article.get('title', 'No title')[:80]
                            print(f"  📝 First result: {title}...")
                    elif 'papers' in result:
                        papers = result['papers']
                        print(f"  📄 Found {len(papers)} papers")
                        if papers:
                            first_paper = papers[0]
                            title = first_paper.get('title', 'No title')[:80]
                            print(f"  📝 First result: {title}...")
                    else:
                        print(f"  📊 Result keys: {list(result.keys())}")
                else:
                    print(f"  📄 Result: {str(result)[:100]}...")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                if "timeout" in str(e).lower():
                    print("  💡 Tip: This search may take longer. Try reducing the 'limit' parameter.")

    print("\n🎉 Literature Search Example completed!")


def main():
    """Main function."""
    literature_search_examples()


if __name__ == "__main__":
    main()
