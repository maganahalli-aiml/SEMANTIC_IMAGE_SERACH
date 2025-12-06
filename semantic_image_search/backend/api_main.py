"""
FastAPI Backend for Semantic Image Search
Provides endpoints for:
- Text-to-Image search
- Image-to-Image search
- Result retrieval and saving
"""

import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from semantic_image_search.backend.retriever import ImageSearchService
from semantic_image_search.backend.config import Config
from semantic_image_search.backend.logger import GLOBAL_LOGGER as log
from semantic_image_search.backend.exception.custom_exception import SemanticImageSearchException


# ============================================================
# PYDANTIC MODELS
# ============================================================

class TextSearchRequest(BaseModel):
    """Request model for text-to-image search
    
    Example:
        {
            "query_text": "yellow flowers",
            "k": 10,
            "metadata_filter": {"category": "nature", "year": 2024},
            "save_results": false
        }
    
    Note: metadata_filter values must be primitives (str, int, bool, float).
    Empty objects {} are not valid.
    """
    query_text: str = Field(..., description="Search query text", examples=["yellow flowers", "sunset over ocean"])
    k: int = Field(default=10, ge=1, le=100, description="Number of results to return")
    metadata_filter: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Optional metadata filters with primitive values (str, int, bool, float). Example: {'category': 'nature', 'year': 2024}",
        examples=[{"category": "nature"}, {"category": "animal", "verified": True}]
    )
    save_results: bool = Field(default=False, description="Whether to save results locally")


class SearchResponse(BaseModel):
    """Response model for search results"""
    query_id: str = Field(..., description="Unique identifier for this search")
    query_type: str = Field(..., description="Type of search: 'text' or 'image'")
    total_results: int = Field(..., description="Number of results found")
    results: List[Dict[str, Any]] = Field(..., description="Search results with scores and metadata")
    saved_path: Optional[str] = Field(None, description="Path where results were saved (if save_results=True)")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    collection: str
    cluster_endpoint: str


# ============================================================
# FASTAPI APP INITIALIZATION
# ============================================================

app = FastAPI(
    title="Semantic Image Search API",
    description="FastAPI backend for text-to-image and image-to-image semantic search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the search service
search_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global search_service
    try:
        log.info("Starting FastAPI backend for Semantic Image Search")
        search_service = ImageSearchService()
        log.info("FastAPI backend started successfully")
    except Exception as e:
        log.error("Failed to start FastAPI backend", error=str(e))
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    log.info("Shutting down FastAPI backend")


# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Semantic Image Search API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        return HealthResponse(
            status="healthy",
            service="Semantic Image Search",
            collection=Config.QDRANT_COLLECTION,
            cluster_endpoint=Config.CLUSTER_API_ENDPOINT
        )
    except Exception as e:
        log.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.post("/search/text", response_model=SearchResponse)
async def search_by_text(request: TextSearchRequest):
    """
    Search for images using text query
    
    Args:
        request: TextSearchRequest containing query_text, k, metadata_filter, and save_results
        
    Returns:
        SearchResponse with results and optional saved path
    """
    query_id = str(uuid.uuid4())
    
    try:
        log.info(
            "Text search request received",
            query_id=query_id,
            query_text=request.query_text,
            k=request.k
        )
        
        # Perform search
        results = search_service.search_by_text(
            query_text=request.query_text,
            k=request.k,
            metadata_filter=request.metadata_filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })
        
        # Save results if requested
        saved_path = None
        if request.save_results and results:
            saved_path = search_service.save_results(results)
            log.info("Results saved", query_id=query_id, saved_path=saved_path)
        
        log.info(
            "Text search completed",
            query_id=query_id,
            total_results=len(results)
        )
        
        return SearchResponse(
            query_id=query_id,
            query_type="text",
            total_results=len(results),
            results=formatted_results,
            saved_path=saved_path
        )
        
    except SemanticImageSearchException as e:
        error_msg = str(e)
        log.error("Text search failed", query_id=query_id, error=error_msg)
        
        # Check if it's an index-related error
        if "Index required but not found" in error_msg:
            # Extract field name from error message
            import re
            field_match = re.search(r'not found for \\"([^"]+)\\"', error_msg)
            field_name = field_match.group(1) if field_match else "field"
            
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "metadata_filter_index_missing",
                    "message": f"Metadata filtering requires a field index on '{field_name}'",
                    "field": field_name,
                    "solution": f"Create an index by running: python -m semantic_image_search.backend.create_indexes",
                    "alternative": "Remove metadata_filter to search without filtering"
                }
            )
        
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        log.error("Unexpected error in text search", query_id=query_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/search/image", response_model=SearchResponse)
async def search_by_image(
    image: UploadFile = File(..., description="Image file to search with"),
    k: int = Query(default=10, ge=1, le=100, description="Number of results to return"),
    save_results: bool = Query(default=False, description="Whether to save results locally"),
    metadata_filter: Optional[str] = Query(default=None, description="JSON string of metadata filters")
):
    """
    Search for similar images using an uploaded image
    
    Args:
        image: Uploaded image file
        k: Number of results to return
        save_results: Whether to save results locally
        metadata_filter: Optional JSON string of metadata filters
        
    Returns:
        SearchResponse with results and optional saved path
    """
    query_id = str(uuid.uuid4())
    temp_image_path = None
    
    try:
        log.info(
            "Image search request received",
            query_id=query_id,
            filename=image.filename,
            k=k
        )
        
        # Save uploaded image temporarily
        temp_dir = Path("/tmp/semantic_search_uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_image_path = temp_dir / f"{query_id}_{image.filename}"
        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        log.info("Image uploaded", query_id=query_id, temp_path=str(temp_image_path))
        
        # Parse metadata filter if provided
        parsed_filter = None
        if metadata_filter:
            import json
            try:
                parsed_filter = json.loads(metadata_filter)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in metadata_filter")
        
        # Perform search
        results = search_service.search_by_image(
            image_path=str(temp_image_path),
            k=k,
            metadata_filter=parsed_filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })
        
        # Save results if requested
        saved_path = None
        if save_results and results:
            saved_path = search_service.save_results(results)
            log.info("Results saved", query_id=query_id, saved_path=saved_path)
        
        log.info(
            "Image search completed",
            query_id=query_id,
            total_results=len(results)
        )
        
        return SearchResponse(
            query_id=query_id,
            query_type="image",
            total_results=len(results),
            results=formatted_results,
            saved_path=saved_path
        )
        
    except SemanticImageSearchException as e:
        error_msg = str(e)
        log.error("Image search failed", query_id=query_id, error=error_msg)
        
        # Check if it's an index-related error
        if "Index required but not found" in error_msg:
            import re
            field_match = re.search(r'not found for \\"([^"]+)\\"', error_msg)
            field_name = field_match.group(1) if field_match else "field"
            
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "metadata_filter_index_missing",
                    "message": f"Metadata filtering requires a field index on '{field_name}'",
                    "field": field_name,
                    "solution": f"Create an index by running: python -m semantic_image_search.backend.create_indexes",
                    "alternative": "Remove metadata_filter to search without filtering"
                }
            )
        
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        log.error("Unexpected error in image search", query_id=query_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        # Clean up temporary file
        if temp_image_path and temp_image_path.exists():
            try:
                os.remove(temp_image_path)
                log.info("Temporary image cleaned up", query_id=query_id)
            except Exception as e:
                log.warning("Failed to clean up temporary image", query_id=query_id, error=str(e))


@app.get("/results/{result_id}")
async def get_saved_results(result_id: str):
    """
    Retrieve saved search results by ID
    
    Args:
        result_id: UUID of the saved search results
        
    Returns:
        JSON with result metadata and list of image paths
    """
    try:
        results_path = Config.RETRIEVED_ROOT / result_id
        
        if not results_path.exists():
            raise HTTPException(status_code=404, detail=f"Results not found: {result_id}")
        
        # List all images in the result directory
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']:
            image_files.extend(results_path.glob(ext))
        
        log.info(
            "Retrieved saved results",
            result_id=result_id,
            image_count=len(image_files)
        )
        
        return {
            "result_id": result_id,
            "path": str(results_path),
            "image_count": len(image_files),
            "images": [f"/results/{result_id}/image/{img.name}" for img in image_files]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error("Failed to retrieve results", result_id=result_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/results/{result_id}/image/{image_name}")
async def get_result_image(result_id: str, image_name: str):
    """
    Retrieve a specific image from saved results
    
    Args:
        result_id: UUID of the saved search results
        image_name: Name of the image file
        
    Returns:
        Image file
    """
    try:
        image_path = Config.RETRIEVED_ROOT / result_id / image_name
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail=f"Image not found: {image_name}")
        
        return FileResponse(
            path=str(image_path),
            media_type=f"image/{image_path.suffix[1:]}",
            filename=image_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(
            "Failed to retrieve image",
            result_id=result_id,
            image_name=image_name,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/metadata/categories")
async def get_available_categories():
    """
    Get list of all available categories from indexed images
    
    Returns:
        List of unique category values
    """
    try:
        from qdrant_client.http import models as qmodels
        
        # Scroll through all points to get unique categories
        scroll_result = search_service.client.scroll(
            collection_name=Config.QDRANT_COLLECTION,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        
        categories = set()
        for point in scroll_result[0]:
            if point.payload and "category" in point.payload:
                categories.add(point.payload["category"])
        
        return {
            "categories": sorted(list(categories)),
            "total_categories": len(categories),
            "note": "These are the available values for metadata_filter.category"
        }
        
    except Exception as e:
        log.error("Failed to get categories", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")


@app.get("/collections/info")
async def get_collection_info():
    """
    Get information about the Qdrant collection
    
    Returns:
        Collection metadata and statistics
    """
    try:
        collection_info = search_service.client.get_collection(Config.QDRANT_COLLECTION)
        
        return {
            "collection_name": Config.QDRANT_COLLECTION,
            "vectors_count": collection_info.vectors_count if hasattr(collection_info, 'vectors_count') else collection_info.points_count,
            "points_count": collection_info.points_count,
            "status": collection_info.status.name if hasattr(collection_info.status, 'name') else str(collection_info.status),
            "config": {
                "vector_size": collection_info.config.params.vectors.get('size') if isinstance(collection_info.config.params.vectors, dict) else collection_info.config.params.vectors.size,
                "distance": str(collection_info.config.params.vectors.get('distance', 'Cosine') if isinstance(collection_info.config.params.vectors, dict) else collection_info.config.params.vectors.distance)
            }
        }
        
    except Exception as e:
        log.error("Failed to get collection info", error=str(e), exception_type=type(e).__name__)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve collection information: {str(e)}")


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
