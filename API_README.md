# FastAPI Backend for Semantic Image Search

A comprehensive REST API for semantic image search with text-to-image and image-to-image retrieval capabilities.

## 🚀 Quick Start

### Start the API Server

```bash
# Option 1: Using the startup script
./run_api.sh

# Option 2: Using uvicorn directly
uvicorn semantic_image_search.backend.api_main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### 1. Health Check
```bash
GET /health
```
Check if the API is running and connected to Qdrant.

**Response:**
```json
{
  "status": "healthy",
  "service": "Semantic Image Search",
  "collection": "semantic-image-search",
  "cluster_endpoint": "https://..."
}
```

---

### 2. Text-to-Image Search
```bash
POST /search/text
```
Search for images using natural language queries.

**Request Body:**
```json
{
  "query_text": "a beautiful sunset over mountains",
  "k": 10,
  "metadata_filter": {
    "category": "landscape"
  },
  "save_results": true
}
```

**Parameters:**
- `query_text` (required): Search query in natural language
- `k` (optional): Number of results (1-100, default: 10)
- `metadata_filter` (optional): Dictionary of metadata filters
- `save_results` (optional): Save results to disk (default: false)

**Response:**
```json
{
  "query_id": "uuid-here",
  "query_type": "text",
  "total_results": 10,
  "results": [
    {
      "id": "image-id",
      "score": 0.95,
      "payload": {
        "image_path": "/path/to/image.jpg",
        "category": "landscape"
      }
    }
  ],
  "saved_path": "/path/to/saved/results"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/search/text" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "sunset over mountains",
    "k": 5,
    "save_results": true
  }'
```

---

### 3. Image-to-Image Search
```bash
POST /search/image
```
Find similar images using an uploaded image.

**Parameters:**
- `image` (required): Image file (multipart/form-data)
- `k` (optional): Number of results (1-100, default: 10)
- `save_results` (optional): Save results to disk (default: false)
- `metadata_filter` (optional): JSON string of metadata filters (must be valid JSON)

**cURL Examples:**
```bash
# Without metadata filter
curl -X POST "http://localhost:8000/search/image" \
  -F "image=@/path/to/your/image.jpg" \
  -F "k=5" \
  -F "save_results=true"

# With metadata filter (category=flower)
curl -X POST "http://localhost:8000/search/image" \
  -F "image=@/path/to/your/image.jpg" \
  -F "k=5" \
  -F 'metadata_filter={"category":"flower"}'
```

**⚠️ Important Note about metadata_filter:**
The `metadata_filter` parameter must be a **valid JSON string**, not a plain string.

✅ Correct:
- `metadata_filter={"category":"flower"}`
- `metadata_filter={"category":"animal","verified":true}`

❌ Incorrect:
- `metadata_filter=uncategorized` (not JSON)
- `metadata_filter=flower` (not JSON)

**Response:**
```json
{
  "query_id": "uuid-here",
  "query_type": "image",
  "total_results": 5,
  "results": [
    {
      "id": "image-id",
      "score": 0.98,
      "payload": {
        "image_path": "/path/to/similar.jpg"
      }
    }
  ],
  "saved_path": "/path/to/saved/results"
}
```

---

### 4. Retrieve Saved Results
```bash
GET /results/{result_id}
```
Get information about saved search results.

**Response:**
```json
{
  "result_id": "uuid-here",
  "path": "/path/to/results",
  "image_count": 5,
  "images": [
    "/results/uuid-here/image/image1.jpg",
    "/results/uuid-here/image/image2.jpg"
  ]
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/results/your-uuid-here"
```

---

### 5. Get Result Image
```bash
GET /results/{result_id}/image/{image_name}
```
Download a specific image from saved results.

**cURL Example:**
```bash
curl "http://localhost:8000/results/your-uuid/image/result_1.jpg" \
  --output downloaded_image.jpg
```

---

### 6. Collection Information
```bash
GET /collections/info
```
Get information about the Qdrant collection.

**Response:**
```json
{
  "collection_name": "semantic-image-search",
  "vectors_count": 1000,
  "points_count": 1000,
  "status": "green",
  "config": {
    "vector_size": 512,
    "distance": "Cosine"
  }
}
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Start the API first
./run_api.sh

# In another terminal, run tests
python test_api.py
```

The test suite will:
1. Check API health
2. Test text-to-image search
3. Test image-to-image search
4. Retrieve saved results
5. Get collection information

---

## 🐍 Python Client Example

```python
import requests

# Text Search
response = requests.post(
    "http://localhost:8000/search/text",
    json={
        "query_text": "golden retriever puppy",
        "k": 10,
        "save_results": True
    }
)
results = response.json()
print(f"Found {results['total_results']} images")

# Image Search
with open("query_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/search/image",
        files={"image": f},
        params={"k": 10, "save_results": True}
    )
results = response.json()
print(f"Found {results['total_results']} similar images")
```

---

## 📊 Features

- ✅ **Text-to-Image Search**: Natural language queries
- ✅ **Image-to-Image Search**: Visual similarity search
- ✅ **Metadata Filtering**: Filter by custom metadata
- ✅ **Result Saving**: Automatic local storage with UUID
- ✅ **Image Retrieval**: Direct access to saved images
- ✅ **CORS Support**: Frontend integration ready
- ✅ **Structured Logging**: Comprehensive request logging
- ✅ **Error Handling**: Custom exception handling
- ✅ **API Documentation**: Interactive Swagger UI

---

## 🔧 Configuration

The API uses the same configuration as the backend:

- **Qdrant Cluster**: Set via `CLUSTER_API_ENDPOINT` in `.env`
- **API Key**: Set via `QDRANT_API_KEY` in `.env`
- **Collection**: Set via `QDRANT_COLLECTION` in `.env`
- **Storage Path**: Set via `RETRIEVED_ROOT` in `.env`

---

## 📝 API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (results/image not found) |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## 🛠️ Development

### Run with auto-reload
```bash
uvicorn semantic_image_search.backend.api_main:app --reload
```

### Run on custom port
```bash
uvicorn semantic_image_search.backend.api_main:app --port 8080
```

### Run with custom host
```bash
uvicorn semantic_image_search.backend.api_main:app --host 0.0.0.0 --port 8000
```

---

## 📦 Dependencies

Required packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `pydantic` - Data validation
- `pillow` - Image processing
- `qdrant-client` - Vector database
- `requests` - HTTP client (for testing)

All dependencies are in `requirements.txt`.

---

## 🚀 Production Deployment

For production, consider:

1. **Use Gunicorn with Uvicorn workers:**
```bash
gunicorn semantic_image_search.backend.api_main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

2. **Configure CORS properly** (update allowed origins)

3. **Add authentication middleware**

4. **Set up rate limiting**

5. **Use environment-specific configs**

6. **Add monitoring and health checks**

---

## 📞 Support

For issues or questions, please check:
- API Documentation: http://localhost:8000/docs
- Health Endpoint: http://localhost:8000/health
- Logs: Check console output for detailed information
