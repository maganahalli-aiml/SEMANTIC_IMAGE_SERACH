#!/usr/bin/env python3
"""
Complete Metadata Filtering Demo
Shows how to use category filters effectively
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("  METADATA FILTERING - COMPLETE DEMO")
print("=" * 80)

# Step 1: Get available categories
print("\n[STEP 1] Discover Available Categories")
print("-" * 80)

response = requests.get(f"{BASE_URL}/metadata/categories")
data = response.json()

print(f"Available categories: {', '.join(data['categories'])}")
print(f"Total categories: {data['total_categories']}")

# Step 2: Search without filter
print("\n[STEP 2] Search WITHOUT Filter (All Categories)")
print("-" * 80)

response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "yellow flowers",
        "k": 5,
        "save_results": False
    }
)

result = response.json()
print(f"Query: 'yellow flowers'")
print(f"Total Results: {result['total_results']}")
print("\nTop 3 Results:")
for i, r in enumerate(result['results'][:3], 1):
    cat = r['payload'].get('category', 'N/A')
    filename = r['payload'].get('filename', 'N/A')
    print(f"  {i}. {filename:25s} Category: {cat:15s} Score: {r['score']:.4f}")

# Step 3: Search WITH filter (category="flower")
print("\n[STEP 3] Search WITH Filter (category='flower')")
print("-" * 80)

response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "yellow flowers",
        "k": 5,
        "metadata_filter": {
            "category": "flower"
        },
        "save_results": False
    }
)

result = response.json()
print(f"Query: 'yellow flowers'")
print(f"Filter: category='flower'")
print(f"Total Results: {result['total_results']}")
print("\nTop 3 Results (All should be flowers):")
for i, r in enumerate(result['results'][:3], 1):
    cat = r['payload'].get('category', 'N/A')
    filename = r['payload'].get('filename', 'N/A')
    print(f"  {i}. {filename:25s} Category: {cat:15s} Score: {r['score']:.4f}")

# Step 4: Search WITH filter (category="animal")
print("\n[STEP 4] Search WITH Filter (category='animal')")
print("-" * 80)

response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "yellow flowers",
        "k": 5,
        "metadata_filter": {
            "category": "animal"
        },
        "save_results": False
    }
)

result = response.json()
print(f"Query: 'yellow flowers'")
print(f"Filter: category='animal'")
print(f"Total Results: {result['total_results']}")
if result['total_results'] > 0:
    print("\nTop 3 Results (All should be animals):")
    for i, r in enumerate(result['results'][:3], 1):
        cat = r['payload'].get('category', 'N/A')
        filename = r['payload'].get('filename', 'N/A')
        print(f"  {i}. {filename:25s} Category: {cat:15s} Score: {r['score']:.4f}")
else:
    print("Note: No animals match 'yellow flowers' query")

# Step 5: Search WITH filter (non-existent category)
print("\n[STEP 5] Search WITH Filter (category='nature' - doesn't exist)")
print("-" * 80)

response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "yellow flowers",
        "k": 5,
        "metadata_filter": {
            "category": "nature"  # This category doesn't exist
        },
        "save_results": False
    }
)

result = response.json()
print(f"Query: 'yellow flowers'")
print(f"Filter: category='nature'")
print(f"Total Results: {result['total_results']}")
print("Note: Returns 0 results because 'nature' category doesn't exist")

# Step 6: Different query with filter
print("\n[STEP 6] Different Query (category='animal')")
print("-" * 80)

response = requests.post(
    f"{BASE_URL}/search/text",
    json={
        "query_text": "wild animals in jungle",
        "k": 5,
        "metadata_filter": {
            "category": "animal"
        },
        "save_results": False
    }
)

result = response.json()
print(f"Query: 'wild animals in jungle'")
print(f"Filter: category='animal'")
print(f"Total Results: {result['total_results']}")
print("\nTop 3 Results:")
for i, r in enumerate(result['results'][:3], 1):
    cat = r['payload'].get('category', 'N/A')
    filename = r['payload'].get('filename', 'N/A')
    print(f"  {i}. {filename:25s} Category: {cat:15s} Score: {r['score']:.4f}")

# Summary
print("\n" + "=" * 80)
print("  KEY TAKEAWAYS")
print("=" * 80)

summary = """
✅ Metadata Filtering Now Works!

1. Field Indexes Created:
   - category (keyword)
   - filename (keyword)
   - verified (bool)
   - year (integer)

2. How to Use Filters:
   
   ✓ Get available categories first:
     GET /metadata/categories
   
   ✓ Use valid category in filter:
     {
       "query_text": "your query",
       "metadata_filter": {"category": "flower"}
     }
   
   ✓ Multiple filters:
     {
       "query_text": "your query",
       "metadata_filter": {
         "category": "flower",
         "verified": true
       }
     }

3. Important Notes:
   
   • Filters only return results that MATCH the filter
   • Non-existent categories return 0 results (not an error)
   • Invalid filter values are skipped (graceful degradation)
   • Always check /metadata/categories to see valid values

4. Available Categories:
   """ + ", ".join(data['categories']) + """

5. cURL Examples:

   # Search all categories
   curl -X POST "http://localhost:8000/search/text" \\
     -H "Content-Type: application/json" \\
     -d '{"query_text": "yellow flowers", "k": 10}'
   
   # Search only flowers
   curl -X POST "http://localhost:8000/search/text" \\
     -H "Content-Type: application/json" \\
     -d '{
       "query_text": "yellow flowers",
       "k": 10,
       "metadata_filter": {"category": "flower"}
     }'
"""

print(summary)

print("\n" + "=" * 80)
print("  ✓ DEMO COMPLETED")
print("=" * 80)
print(f"\n📚 API Documentation: {BASE_URL}/docs")
print(f"📋 Available Categories: {BASE_URL}/metadata/categories")
