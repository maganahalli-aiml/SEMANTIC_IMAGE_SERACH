import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List

from qdrant_client.http import models
from PIL import Image

from semantic_image_search.backend.config import Config
from semantic_image_search.backend.qdrant_client import QdrantClientManager
from semantic_image_search.backend.embeddings import (
    embed_text,
    embed_single_image,
)
from semantic_image_search.backend.logger import GLOBAL_LOGGER as log
from semantic_image_search.backend.exception.custom_exception import SemanticImageSearchException


class ImageSearchService:
    """
    High-level abstraction for semantic image search.
    Handles:
      - Text → Image retrieval
      - Image → Image retrieval
      - Saving retrieved results
    """

    def __init__(self):
        log.info("Initializing ImageSearchService")

        try:
            # Load and ensure Qdrant collection
            self.client = QdrantClientManager.get_client()
            QdrantClientManager.ensure_collection()

            self.collection = Config.QDRANT_COLLECTION
            self.retrieved_root = Config.RETRIEVED_ROOT

            log.info(
                "ImageSearchService initialized",
                collection=self.collection,
                retrieved_root=str(self.retrieved_root)
            )

        except Exception as e:
            log.error("Failed to initialize ImageSearchService", error=str(e))
            raise SemanticImageSearchException("Failed to initialize ImageSearchService", e)

    # ------------------------------------------------------------------
    # TEXT → IMAGE SEARCH
    # ------------------------------------------------------------------
    def search_by_text(
        self,
        query_text: str,
        k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[models.ScoredPoint]:
        """
        Search for images using text query.
        
        Args:
            query_text: Natural language or caption text query
            k: Number of top results to return (default: 5)
            metadata_filter: Optional dict for filtering by metadata fields
            
        Returns:
            List of ScoredPoint objects with image metadata and scores
            
        Raises:
            SemanticImageSearchException: If search fails
        """
        log.info(
            "Text search started",
            query_text=query_text,
            top_k=k,
            filter=metadata_filter
        )

        try:
            # Convert text query into embedding vector
            vector = embed_text(query_text)

            # Construct metadata filter (optional)
            q_filter = None
            if metadata_filter:
                must_conditions = []
                for key, value in metadata_filter.items():
                    # Skip invalid or empty values
                    if value is None or value == {} or value == []:
                        log.warning(
                            "Skipping invalid metadata filter value",
                            key=key,
                            value=value
                        )
                        continue
                    
                    # Validate value type
                    if not isinstance(value, (str, int, bool, float)):
                        log.warning(
                            "Skipping non-primitive metadata filter value",
                            key=key,
                            value_type=type(value).__name__
                        )
                        continue
                    
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )

                # Only set filter if we have valid conditions
                if must_conditions:
                    q_filter = models.Filter(must=must_conditions)
                else:
                    log.info("No valid metadata filter conditions, searching without filter")

            # Perform vector search
            results = self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=k,
                query_filter=q_filter,
                with_payload=True,
                with_vectors=False
            ).points

            log.info(
                "Text search completed",
                query_text=query_text,
                total_results=len(results)
            )

            return results

        except Exception as e:
            log.error("Text search failed", query_text=query_text, error=str(e))
            raise SemanticImageSearchException("Text search failed", e)

    # ------------------------------------------------------------------
    # IMAGE → IMAGE SEARCH
    # ------------------------------------------------------------------
    def search_by_image(
        self,
        image_path: str,
        k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[models.ScoredPoint]:
        """
        Search for similar images using an image query.
        
        Args:
            image_path: Path to query image file
            k: Number of top results to return (default: 5)
            metadata_filter: Optional dict for filtering by metadata fields
            
        Returns:
            List of ScoredPoint objects with similar image metadata and scores
            
        Raises:
            SemanticImageSearchException: If search fails
        """
        log.info(
            "Image search started",
            image_path=image_path,
            top_k=k,
            filter=metadata_filter
        )

        try:
            # Convert image into embedding vector
            vector = embed_single_image(image_path)

            # Build filter only if metadata_filter provided
            q_filter = None
            if metadata_filter:
                must_conditions = []
                for key, value in metadata_filter.items():
                    # Skip invalid or empty values
                    if value is None or value == {} or value == []:
                        log.warning(
                            "Skipping invalid metadata filter value",
                            key=key,
                            value=value
                        )
                        continue
                    
                    # Validate value type
                    if not isinstance(value, (str, int, bool, float)):
                        log.warning(
                            "Skipping non-primitive metadata filter value",
                            key=key,
                            value_type=type(value).__name__
                        )
                        continue
                    
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )

                # Only set filter if we have valid conditions
                if must_conditions:
                    q_filter = models.Filter(must=must_conditions)
                else:
                    log.info("No valid metadata filter conditions, searching without filter")

            # Perform vector search
            results = self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=k,
                query_filter=q_filter,
                with_payload=True,
                with_vectors=False
            ).points

            log.info(
                "Image search completed",
                image_path=image_path,
                total_results=len(results)
            )

            return results

        except Exception as e:
            log.error("Image search failed", image_path=image_path, error=str(e))
            raise SemanticImageSearchException("Image search failed", e)

    # ------------------------------------------------------------------
    # SAVE RETRIEVED IMAGES LOCALLY
    # ------------------------------------------------------------------
    def save_results(self, results: List[models.ScoredPoint]) -> str:
        """
        Save retrieved images to local directory.
        
        Args:
            results: List of ScoredPoint objects from search
            
        Returns:
            String path to output directory containing saved images
            
        Raises:
            SemanticImageSearchException: If saving fails
        """
        output_dir = Path(self.retrieved_root) / uuid.uuid4().hex

        log.info(
            "Saving retrieved results",
            total_results=len(results),
            output_dir=str(output_dir)
        )

        try:
            output_dir.mkdir(parents=True, exist_ok=True)

            for idx, point in enumerate(results):
                src_path = point.payload["path"]
                img = Image.open(src_path)
                img.save(output_dir / f"result_{idx}.png")

            log.info("Results saved successfully", output_dir=str(output_dir))
            return str(output_dir)

        except Exception as e:
            log.error("Failed to save results", output_dir=str(output_dir), error=str(e))
            raise SemanticImageSearchException("Failed to save results", e)
