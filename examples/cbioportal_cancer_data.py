#!/usr/bin/env python3
"""
cBioPortal Cancer Data Analysis Example

This example shows how to use the cBioPortal tool to query cancer genomics
data from The Cancer Genome Atlas (TCGA) and other studies.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.tooluniverse import ToolUniverse

def main():
    # Initialize ToolUniverse
    tu = ToolUniverse()
    
    # Load tools first
    tu.load_tools()
    
    print("🎗️ cBioPortal Cancer Data Analysis Examples")
    print("=" * 50)
    
    # Example 1: Query TCGA breast cancer studies
    print("\n1. Querying TCGA breast cancer studies")
    print("-" * 40)
    
    result = tu.run({"name": "cBioPortal_get_cancer_studies", "arguments": {
        "limit": 5
    }})
    
    if result and result.get("status") == "success":
        data = result.get("data", [])
        print(f"✅ Found {len(data)} cancer studies")
        
        for i, study in enumerate(data[:3], 1):
            study_id = study.get("studyId", "Unknown")
            name = study.get("name", "Unknown")
            print(f"   {i}. {study_id}: {name}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Example 2: Query specific cancer types
    print("\n2. Querying specific cancer types")
    print("-" * 35)
    
    # This would typically use a different endpoint for specific cancer types
    # For now, we'll use the general studies endpoint
    result = tu.run({"name": "cBioPortal_get_cancer_studies", "arguments": {
        "limit": 10
    }})
    
    if result and result.get("status") == "success":
        data = result.get("data", [])
        print(f"✅ Found {len(data)} studies")
        
        # Show different cancer types
        cancer_types = set()
        for study in data:
            cancer_type = study.get("cancerTypeId", "Unknown")
            cancer_types.add(cancer_type)
        
        print(f"   Cancer types found: {', '.join(list(cancer_types)[:5])}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Example 3: Query studies with specific criteria
    print("\n3. Querying studies with specific criteria")
    print("-" * 40)
    
    result = tu.run({"name": "cBioPortal_get_cancer_studies", "arguments": {
        "limit": 8
    }})
    
    if result and result.get("status") == "success":
        data = result.get("data", [])
        print(f"✅ Found {len(data)} studies")
        
        # Show studies with specific characteristics
        for i, study in enumerate(data[:3], 1):
            study_id = study.get("studyId", "Unknown")
            name = study.get("name", "Unknown")
            description = study.get("description", "No description")
            print(f"   {i}. {study_id}")
            print(f"      Name: {name}")
            print(f"      Description: {description[:100]}...")

if __name__ == "__main__":
    main()
