"""
Test script for Semantic Image Search FastAPI Backend
Demonstrates API usage for text-to-image and image-to-image search
"""

import requests
import json
from pathlib import Path

# API Base URL
BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("1. HEALTH CHECK")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_text_search():
    """Test text-to-image search"""
    print("\n" + "="*60)
    print("2. TEXT-TO-IMAGE SEARCH")
    print("="*60)
    
    payload = {
        "query_text": "a beautiful sunset over mountains",
        "k": 5,
        "save_results": True
    }
    
    print(f"Query: {payload['query_text']}")
    print(f"Requesting {payload['k']} results...")
    
    response = requests.post(f"{BASE_URL}/search/text", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Query ID: {result['query_id']}")
        print(f"Total Results: {result['total_results']}")
        print(f"Saved Path: {result.get('saved_path', 'N/A')}")
        
        if result['results']:
            print("\nTop 3 Results:")
            for i, res in enumerate(result['results'][:3], 1):
                print(f"  {i}. Score: {res['score']:.4f}")
                print(f"     ID: {res['id']}")
                if res.get('payload'):
                    print(f"     Metadata: {json.dumps(res['payload'], indent=8)}")
        
        return result.get('saved_path')
    else:
        print(f"Error: {response.text}")
        return None


def test_image_search(image_path: str):
    """Test image-to-image search"""
    print("\n" + "="*60)
    print("3. IMAGE-TO-IMAGE SEARCH")
    print("="*60)
    
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        print("Skipping image search test...")
        return None
    
    print(f"Using image: {image_path}")
    
    with open(image_path, 'rb') as f:
        files = {'image': (Path(image_path).name, f, 'image/jpeg')}
        params = {
            'k': 5,
            'save_results': True
        }
        
        response = requests.post(f"{BASE_URL}/search/image", files=files, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Query ID: {result['query_id']}")
        print(f"Total Results: {result['total_results']}")
        print(f"Saved Path: {result.get('saved_path', 'N/A')}")
        
        if result['results']:
            print("\nTop 3 Results:")
            for i, res in enumerate(result['results'][:3], 1):
                print(f"  {i}. Score: {res['score']:.4f}")
                print(f"     ID: {res['id']}")
        
        return result.get('saved_path')
    else:
        print(f"Error: {response.text}")
        return None


def test_get_saved_results(result_id: str):
    """Test retrieving saved results"""
    print("\n" + "="*60)
    print("4. RETRIEVE SAVED RESULTS")
    print("="*60)
    
    if not result_id:
        print("No result ID provided, skipping...")
        return
    
    # Extract UUID from path
    result_uuid = Path(result_id).name
    
    print(f"Result ID: {result_uuid}")
    
    response = requests.get(f"{BASE_URL}/results/{result_uuid}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Path: {result['path']}")
        print(f"Image Count: {result['image_count']}")
        
        if result['images']:
            print(f"\nFirst 3 images:")
            for i, img_url in enumerate(result['images'][:3], 1):
                print(f"  {i}. {img_url}")
    else:
        print(f"Error: {response.text}")


def test_collection_info():
    """Test collection information endpoint"""
    print("\n" + "="*60)
    print("5. COLLECTION INFORMATION")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/collections/info")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        info = response.json()
        print(f"Collection Name: {info['collection_name']}")
        print(f"Points Count: {info['points_count']}")
        print(f"Vectors Count: {info['vectors_count']}")
        print(f"Status: {info['status']}")
        print(f"Vector Config: {json.dumps(info['config'], indent=2)}")
    else:
        print(f"Error: {response.text}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SEMANTIC IMAGE SEARCH API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Health check failed. Is the API running?")
        print("Run: ./run_api.sh or python -m uvicorn semantic_image_search.backend.api_main:app")
        return
    
    print("\n✓ Health check passed!")
    
    # Test 2: Text Search
    text_result_path = test_text_search()
    
    # Test 3: Image Search (use first image from data folder if available)
    data_dir = Path("data")
    test_image = None
    if data_dir.exists():
        image_files = list(data_dir.rglob("*.jpg")) + list(data_dir.rglob("*.png"))
        if image_files:
            test_image = str(image_files[0])
    
    image_result_path = test_image_search(test_image) if test_image else None
    
    # Test 4: Get Saved Results
    if text_result_path:
        test_get_saved_results(text_result_path)
    elif image_result_path:
        test_get_saved_results(image_result_path)
    
    # Test 5: Collection Info
    test_collection_info()
    
    print("\n" + "="*60)
    print("✓ ALL TESTS COMPLETED")
    print("="*60)
    print(f"\n📚 API Documentation: {BASE_URL}/docs")
    print(f"📖 ReDoc: {BASE_URL}/redoc")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API. Please start the server first:")
        print("   ./run_api.sh")
        print("   or")
        print("   python -m uvicorn semantic_image_search.backend.api_main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
