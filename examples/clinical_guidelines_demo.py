#!/usr/bin/env python3
"""
Clinical Guidelines Tools - Complete Demo

Demonstrates searching and extracting clinical guidelines from multiple sources.
Includes 6 search tools and 2 full-text extraction tools.
"""

from tooluniverse import ToolUniverse


def demo_search(tu):
    """Demo: Search guidelines from multiple sources"""
    print("=" * 80)
    print("DEMO 1: Multi-Source Guideline Search")
    print("=" * 80)
    
    query = "diabetes"
    print(f"\nSearching for '{query}' across 6 sources...")
    
    # Search NICE (UK)
    print(f"\n1. NICE (UK Official Guidelines):")
    results = tu.run({
        "name": "NICE_Clinical_Guidelines_Search",
        "arguments": {"query": query, "limit": 2}
    })
    for i, g in enumerate(results[:2], 1):
        print(f"   {i}. {g['title']}")
        print(f"      {g['url']}")
    
    # Search PubMed (Peer-reviewed)
    print(f"\n2. PubMed (Peer-Reviewed):")
    results = tu.run({
        "name": "PubMed_Guidelines_Search",
        "arguments": {"query": query, "limit": 2}
    })
    if isinstance(results, dict) and 'guidelines' in results:
        results = results['guidelines']
    for i, g in enumerate(results[:2], 1):
        print(f"   {i}. {g['title'][:70]}...")
        print(f"      PMID: {g['pmid']}")
    
    # Search WHO (International)
    print(f"\n3. WHO (International):")
    results = tu.run({
        "name": "WHO_Guidelines_Search",
        "arguments": {"query": query, "limit": 2}
    })
    if isinstance(results, dict) and 'guidelines' in results:
        results = results['guidelines']
    for i, g in enumerate(results[:2], 1):
        print(f"   {i}. {g['title']}")
        print(f"      {g['url']}")
    
    print("\n✓ Also available: Europe PMC, TRIP Database, OpenAlex")


def demo_fulltext_nice(tu):
    """Demo: Extract full text from NICE guideline"""
    print("\n" + "=" * 80)
    print("DEMO 2: NICE Full-Text Extraction")
    print("=" * 80)
    
    # Step 1: Search
    print("\nSearching for NICE guideline...")
    results = tu.run({
        "name": "NICE_Clinical_Guidelines_Search",
        "arguments": {"query": "type 2 diabetes", "limit": 1}
    })
    
    if not results:
        print("No results found")
        return
    
    guideline = results[0]
    print(f"Found: {guideline['title']}")
    print(f"URL: {guideline['url']}")
    
    # Step 2: Extract full text
    print("\nExtracting full guideline text...")
    full_text = tu.run({
        "name": "NICE_Guideline_Full_Text",
        "arguments": {"url": guideline['url']}
    })
    
    print(f"\n✓ Success!")
    print(f"  Length: {full_text['full_text_length']:,} characters")
    print(f"  Sections: {full_text['sections_count']}")
    print(f"  Recommendations: {full_text['recommendations_count']}")
    print(f"\n  Preview:\n  {full_text['full_text'][:250].replace(chr(10), chr(10) + '  ')}...")


def demo_fulltext_who(tu):
    """Demo: Extract content and PDF from WHO guideline"""
    print("\n" + "=" * 80)
    print("DEMO 3: WHO Full-Text + PDF Extraction")
    print("=" * 80)
    
    # Step 1: Search
    print("\nSearching for WHO guideline...")
    results = tu.run({
        "name": "WHO_Guidelines_Search",
        "arguments": {"query": "HIV", "limit": 1}
    })
    
    if isinstance(results, dict) and 'guidelines' in results:
        results = results['guidelines']
    
    if not results:
        print("No results found")
        return
    
    guideline = results[0]
    print(f"Found: {guideline['title']}")
    print(f"URL: {guideline['url']}")
    
    # Step 2: Extract content
    print("\nExtracting content and PDF link...")
    content = tu.run({
        "name": "WHO_Guideline_Full_Text",
        "arguments": {"url": guideline['url']}
    })
    
    print(f"\n✓ Success!")
    print(f"  Content length: {content['content_length']:,} characters")
    print(f"  Has PDF: {content['has_pdf']}")
    if content['has_pdf']:
        print(f"  PDF URL: {content['pdf_download_url']}")
    if content.get('overview'):
        print(f"\n  Overview:\n  {content['overview'][:200].replace(chr(10), chr(10) + '  ')}...")


def demo_comparison(tu):
    """Demo: Compare results from different sources"""
    print("\n" + "=" * 80)
    print("DEMO 4: Multi-Source Comparison")
    print("=" * 80)
    
    query = "hypertension"
    print(f"\nComparing results for '{query}':")
    
    sources = [
        ("NICE", "NICE_Clinical_Guidelines_Search"),
        ("PubMed", "PubMed_Guidelines_Search"),
        ("WHO", "WHO_Guidelines_Search"),
        ("Europe PMC", "EuropePMC_Guidelines_Search"),
    ]
    
    total = 0
    for name, tool_name in sources:
        results = tu.run({
            "name": tool_name,
            "arguments": {"query": query, "limit": 3}
        })
        if isinstance(results, dict) and 'guidelines' in results:
            results = results['guidelines']
        
        count = len(results) if isinstance(results, list) else 0
        total += count
        print(f"  {name:15} {count} guidelines")
        
        if results and isinstance(results, list):
            print(f"    → {results[0]['title'][:60]}...")
    
    print(f"\n✓ Total found: {total} guidelines across 4 sources")


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("CLINICAL GUIDELINES TOOLS - COMPLETE DEMO")
    print("=" * 80)
    print("\n8 Tools Available:")
    print("  • 6 Search Tools: NICE, WHO, PubMed, Europe PMC, TRIP, OpenAlex")
    print("  • 2 Full-Text Tools: NICE & WHO complete content extraction")
    
    # Initialize
    print("\nInitializing ToolUniverse...")
    tu = ToolUniverse()
    tu.load_tools()
    print(f"✓ Loaded {len(tu.all_tool_dict)} tools\n")
    
    try:
        # Run all demos
        demo_search(tu)
        demo_fulltext_nice(tu)
        demo_fulltext_who(tu)
        demo_comparison(tu)
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print("\n✅ All demos completed successfully!")
        print("\nKey Features:")
        print("  • Search 6 authoritative guideline sources")
        print("  • Extract complete full-text from NICE (5,000+ chars)")
        print("  • Extract content + PDF links from WHO (1,500+ chars)")
        print("  • Access peer-reviewed guidelines from PubMed/Europe PMC")
        print("  • Compare results across multiple databases")
        print("\nUsage:")
        print("  from tooluniverse import ToolUniverse")
        print("  tu = ToolUniverse()")
        print("  tu.load_tools()")
        print("  results = tu.run({'name': 'NICE_Clinical_Guidelines_Search',")
        print("                     'arguments': {'query': 'diabetes', 'limit': 5}})")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
