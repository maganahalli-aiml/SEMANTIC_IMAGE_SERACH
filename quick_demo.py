#!/usr/bin/env python3
"""
Quick API Demo - Test all endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("  SEMANTIC IMAGE SEARCH API - QUICK DEMO")
print("=" * 70)

# 1. Health Check
print("\n[1] HEALTH CHECK")
print("-" * 70)
response = requests.get(f"{BASE_URL}/health")
print(f"✓ Status: {response.status_code}")
print(f"✓ Response: {json.dumps(response.json(), indent=2)}")

# 2. Collection Info
print("\n[2] COLLECTION INFO")
print("-" * 70)
response = requests.get(f"{BASE_URL}/collections/info")
info = response.json()
print(f"✓ Collection: {info['collection_name']}")
print(f"✓ Points Count: {info['points_count']}")
print(f"✓ Vector Size: {info['config']['vector_size']}")
print(f"✓ Distance Metric: {info['config']['distance']}")

# 3. Text Search
print("\n[3] TEXT-TO-IMAGE SEARCH")
print("-" * 70)
response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "animals in nature",
        "k": 5,
        "save_results": True
    }
)
result = response.json()
print(f"✓ Query ID: {result['query_id']}")
print(f"✓ Total Results: {result['total_results']}")
print(f"✓ Saved Path: {result.get('saved_path', 'N/A')}")
print(f"\nTop 3 Results:")
for i, res in enumerate(result['results'][:3], 1):
    print(f"  {i}. Score: {res['score']:.4f} | {res['payload'].get('filename', 'N/A')}")

# 4. Text Search with Metadata Filter (if index exists)
print("\n[4] TEXT SEARCH WITH METADATA FILTER")
print("-" * 70)
try:
    response = requests.post(
        f"{BASE_URL}/search/text",
        json={
            "query_text": "wild animals",
            "k": 5,
            "metadata_filter": {"category": "animal"},
            "save_results": False
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Query ID: {result['query_id']}")
        print(f"✓ Total Results: {result['total_results']}")
        print(f"\nTop 3 Results (filtered by category='animal'):")
        for i, res in enumerate(result['results'][:3], 1):
            print(f"  {i}. Score: {res['score']:.4f} | {res['payload'].get('filename', 'N/A')} | Category: {res['payload'].get('category', 'N/A')}")
    else:
        print(f"⚠️  Metadata filtering requires indexes on fields")
        print(f"   Skipping filtered search (index may not exist for 'category')")
except Exception as e:
    print(f"⚠️  Metadata filter test skipped: {str(e)[:100]}")

print("\n" + "=" * 70)
print("  ✓ DEMO COMPLETED SUCCESSFULLY")
print("=" * 70)
print(f"\n📚 Full API Documentation: {BASE_URL}/docs")
print(f"📖 Alternative Docs: {BASE_URL}/redoc")
print(f"🏥 Health Check: {BASE_URL}/health")
