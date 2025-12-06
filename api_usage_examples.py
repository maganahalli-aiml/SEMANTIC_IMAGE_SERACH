#!/usr/bin/env python3
"""
API Usage Examples - Correct and Incorrect Patterns
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("  SEMANTIC IMAGE SEARCH API - USAGE EXAMPLES")
print("=" * 80)

# ============================================================================
# ✅ CORRECT: Text search without metadata filter
# ============================================================================
print("\n[✅ CORRECT] Text search without metadata filter")
print("-" * 80)

request_data = {
    "query_text": "yellow flowers",
    "k": 5,
    "save_results": False
}

print(f"Request:\n{json.dumps(request_data, indent=2)}")

response = requests.post(f"{BASE_URL}/search/text", json=request_data)
result = response.json()

print(f"\nResponse: ✓ Success")
print(f"  - Query ID: {result['query_id']}")
print(f"  - Total Results: {result['total_results']}")
print(f"  - Top Result: {result['results'][0]['payload']['filename']} (score: {result['results'][0]['score']:.4f})")


# ============================================================================
# ❌ INCORRECT: Metadata filter with empty object (Swagger default)
# ============================================================================
print("\n\n[❌ INCORRECT - BUT NOW HANDLED] Metadata filter with empty object")
print("-" * 80)

request_data = {
    "query_text": "yellow flowers",
    "k": 5,
    "metadata_filter": {
        "additionalProp1": {}  # ❌ Empty object - invalid
    },
    "save_results": False
}

print(f"Request:\n{json.dumps(request_data, indent=2)}")
print("\nNote: Empty objects {} are invalid but now gracefully handled")

response = requests.post(f"{BASE_URL}/search/text", json=request_data)
result = response.json()

print(f"\nResponse: ✓ Success (invalid filter ignored)")
print(f"  - Query ID: {result['query_id']}")
print(f"  - Total Results: {result['total_results']}")
print(f"  - Behavior: Search executed without filter")


# ============================================================================
# ✅ CORRECT: Metadata filter with valid string value
# ============================================================================
print("\n\n[✅ CORRECT] Metadata filter with valid string value")
print("-" * 80)

request_data = {
    "query_text": "animals",
    "k": 5,
    "metadata_filter": {
        "category": "flower"  # ✅ Valid string value
    },
    "save_results": False
}

print(f"Request:\n{json.dumps(request_data, indent=2)}")
print("\nNote: This requires a keyword index on 'category' field in Qdrant")

response = requests.post(f"{BASE_URL}/search/text", json=request_data)

if response.status_code == 200:
    result = response.json()
    print(f"\nResponse: ✓ Success")
    print(f"  - Query ID: {result['query_id']}")
    print(f"  - Total Results: {result['total_results']}")
    print(f"  - All results have category='flower'")
else:
    print(f"\nResponse: ⚠️ Failed (index may not exist)")
    print(f"  - Error: Field index required for metadata filtering")


# ============================================================================
# ✅ CORRECT: Multiple metadata filters
# ============================================================================
print("\n\n[✅ CORRECT] Multiple metadata filters with valid values")
print("-" * 80)

request_data = {
    "query_text": "landscape",
    "k": 5,
    "metadata_filter": {
        "category": "nature",    # ✅ Valid string
        "verified": True,        # ✅ Valid boolean
        "year": 2024            # ✅ Valid integer
    },
    "save_results": False
}

print(f"Request:\n{json.dumps(request_data, indent=2)}")
print("\nNote: All values are primitives (str, int, bool)")

response = requests.post(f"{BASE_URL}/search/text", json=request_data)
print(f"\nResponse: {response.status_code}")


# ============================================================================
# SUMMARY OF RULES
# ============================================================================
print("\n\n" + "=" * 80)
print("  METADATA FILTER RULES")
print("=" * 80)

rules = """
✅ VALID Values:
   - Strings:   "flower", "nature", "2024"
   - Integers:  2024, 42, 100
   - Booleans:  true, false
   - Floats:    3.14, 0.5

❌ INVALID Values:
   - Empty objects:  {}
   - Arrays:         []
   - Nested objects: {"key": "value"}
   - null/None:      null

📝 Examples:

   ✅ CORRECT:
   {
     "metadata_filter": {
       "category": "flower",
       "year": 2024,
       "verified": true
     }
   }

   ❌ INCORRECT (Swagger default):
   {
     "metadata_filter": {
       "additionalProp1": {},    // Empty object
       "additionalProp2": {},    // Empty object
       "additionalProp3": {}     // Empty object
     }
   }

   ✅ CORRECT (no filter):
   {
     "metadata_filter": null
   }
   
   // OR simply omit the field:
   {
     "query_text": "flowers",
     "k": 10
   }

⚠️  Important Notes:
   - Metadata filtering requires field indexes in Qdrant
   - Invalid filter values are now automatically skipped
   - If all filters are invalid, search proceeds without filtering
   - Check Qdrant logs if filtering doesn't work as expected
"""

print(rules)

print("\n" + "=" * 80)
print("  ✓ EXAMPLES COMPLETED")
print("=" * 80)
print(f"\n📚 API Documentation: {BASE_URL}/docs")
print("💡 Tip: Use the 'Try it out' feature carefully in Swagger UI")
print("💡 Tip: Remove the example 'additionalProp' fields before testing")
