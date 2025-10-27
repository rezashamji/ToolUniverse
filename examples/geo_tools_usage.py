#!/usr/bin/env python3
"""
Usage examples for GEO tools in ToolUniverse

This script demonstrates how to use the GEO database tools for gene expression
dataset search, metadata retrieval, and sample information analysis.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.tooluniverse import ToolUniverse

def example_search_datasets():
    """Search for cancer-related datasets in human"""
    print("🔍 Searching for cancer datasets in human...")
    
    tu = ToolUniverse()
    tu.load_tools()
    
    result = tu.run({
        "name": "geo_search_datasets",
        "arguments": {
            "query": "cancer",
            "organism": "Homo sapiens",
            "limit": 10
        }
    })
    
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        data = result.get('data', {})
        esearch = data.get('esearchresult', {})
        print(f"Found {esearch.get('count')} datasets")
        idlist = esearch.get('idlist', [])
        print(f"Dataset IDs: {idlist[:5]}")  # Show first 5
    else:
        print(f"Error: {result.get('error')}")
    
    return result

def example_search_by_study_type():
    """Search for microarray datasets"""
    print("\n🔍 Searching for microarray datasets...")
    
    tu = ToolUniverse()
    tu.load_tools()
    
    result = tu.run({
        "name": "geo_search_datasets",
        "arguments": {
            "query": "diabetes",
            "study_type": "Expression profiling by array",
            "limit": 5
        }
    })
    
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        data = result.get('data', {})
        esearch = data.get('esearchresult', {})
        print(f"Found {esearch.get('count')} microarray datasets")
        idlist = esearch.get('idlist', [])
        print(f"Dataset IDs: {idlist}")
    else:
        print(f"Error: {result.get('error')}")
    
    return result

def example_get_dataset_info():
    """Get detailed information for a dataset"""
    print("\n📊 Getting dataset information...")
    
    tu = ToolUniverse()
    tu.load_tools()
    
    # Use a known GEO dataset ID (this is an example)
    result = tu.run({
        "name": "geo_get_dataset_info",
        "arguments": {
            "dataset_id": "GDS1234"  # Example dataset ID
        }
    })
    
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        data = result.get('data', {})
        result_data = data.get('result', {})
        if result_data:
            print(f"Dataset UID: {result_data.get('uid')}")
            print(f"Title: {result_data.get('title')}")
            print(f"Organism: {result_data.get('organism')}")
            print(f"Platform: {result_data.get('platform')}")
        else:
            print("No dataset information found")
    else:
        print(f"Error: {result.get('error')}")
    
    return result

def example_get_sample_info():
    """Get sample information for a dataset"""
    print("\n🧬 Getting sample information...")
    
    tu = ToolUniverse()
    tu.load_tools()
    
    result = tu.run({
        "name": "geo_get_sample_info",
        "arguments": {
            "dataset_id": "GDS1234"  # Example dataset ID
        }
    })
    
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        data = result.get('data', {})
        result_data = data.get('result', {})
        if result_data:
            print(f"Dataset UID: {result_data.get('uid')}")
            samples = result_data.get('samples', [])
            print(f"Number of samples: {len(samples)}")
            for i, sample in enumerate(samples[:3]):  # Show first 3
                print(f"  Sample {i+1}: {sample.get('sample_id')} - {sample.get('characteristics')}")
        else:
            print("No sample information found")
    else:
        print(f"Error: {result.get('error')}")
    
    return result

def example_combined_search():
    """Search for datasets and get info for the first result"""
    print("\n🔗 Combined search and info retrieval...")
    
    tu = ToolUniverse()
    tu.load_tools()
    
    # First search for datasets
    search_result = tu.run({
        "name": "geo_search_datasets",
        "arguments": {
            "query": "breast cancer",
            "organism": "Homo sapiens",
            "limit": 3
        }
    })
    
    if search_result.get('status') == 'success':
        data = search_result.get('data', {})
        esearch = data.get('esearchresult', {})
        idlist = esearch.get('idlist', [])
        
        if idlist:
            print(f"Found {len(idlist)} datasets, getting info for first one...")
            
            # Get info for first dataset
            info_result = tu.run({
                "name": "geo_get_dataset_info",
                "arguments": {
                    "dataset_id": idlist[0]
                }
            })
            
            print(f"Info status: {info_result.get('status')}")
            if info_result.get('status') == 'success':
                info_data = info_result.get('data', {})
                result_data = info_data.get('result', {})
                if result_data:
                    print(f"Dataset: {result_data.get('title')}")
                    print(f"Organism: {result_data.get('organism')}")
            else:
                print(f"Error getting info: {info_result.get('error')}")
        else:
            print("No datasets found")
    else:
        print(f"Search failed: {search_result.get('error')}")
    
    return search_result

def main():
    """Run all GEO tool examples"""
    print("🚀 GEO Tools Usage Examples")
    print("=" * 40)
    
    try:
        # Run examples
        example_search_datasets()
        example_search_by_study_type()
        example_get_dataset_info()
        example_get_sample_info()
        example_combined_search()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
