"""
Utility to create field indexes in Qdrant for metadata filtering
"""

from qdrant_client.http import models
from semantic_image_search.backend.qdrant_client import QdrantClientManager
from semantic_image_search.backend.config import Config
from semantic_image_search.backend.logger import GLOBAL_LOGGER as log


def create_field_indexes():
    """
    Create payload indexes in Qdrant collection to enable metadata filtering.
    
    Without these indexes, filtering by metadata fields will fail with:
    "Index required but not found for field"
    """
    
    client = QdrantClientManager.get_client()
    collection_name = Config.QDRANT_COLLECTION
    
    log.info("Creating field indexes for metadata filtering", collection=collection_name)
    
    # Define fields to index
    fields_to_index = [
        ("category", models.PayloadSchemaType.KEYWORD),
        ("filename", models.PayloadSchemaType.KEYWORD),
        ("verified", models.PayloadSchemaType.BOOL),
        ("year", models.PayloadSchemaType.INTEGER),
    ]
    
    for field_name, field_type in fields_to_index:
        try:
            log.info(f"Creating index for field: {field_name}", field_type=field_type.value)
            
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field_name,
                field_schema=field_type,
                wait=True
            )
            
            log.info(f"✓ Index created successfully for: {field_name}")
            
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                log.info(f"✓ Index already exists for: {field_name}")
            else:
                log.error(f"Failed to create index for: {field_name}", error=error_msg)
                raise
    
    log.info("All field indexes created successfully")
    print("\n" + "="*70)
    print("✓ Field indexes created successfully!")
    print("="*70)
    print("\nYou can now use metadata filtering with these fields:")
    for field_name, field_type in fields_to_index:
        print(f"  - {field_name}: {field_type.value}")
    print("\nExample request:")
    print("""
    {
      "query_text": "yellow flowers",
      "k": 10,
      "metadata_filter": {
        "category": "flower",
        "verified": true
      }
    }
    """)


def list_existing_indexes():
    """List all existing field indexes in the collection"""
    
    client = QdrantClientManager.get_client()
    collection_name = Config.QDRANT_COLLECTION
    
    log.info("Fetching existing indexes", collection=collection_name)
    
    collection_info = client.get_collection(collection_name)
    
    print("\n" + "="*70)
    print(f"Collection: {collection_name}")
    print("="*70)
    
    if hasattr(collection_info, 'payload_schema') and collection_info.payload_schema:
        print("\nExisting Field Indexes:")
        for field_name, field_info in collection_info.payload_schema.items():
            print(f"  ✓ {field_name}: {field_info}")
    else:
        print("\n⚠️  No field indexes found")
        print("   Run: python -m semantic_image_search.backend.create_indexes")
    
    print("="*70)


def delete_field_index(field_name: str):
    """Delete a specific field index"""
    
    client = QdrantClientManager.get_client()
    collection_name = Config.QDRANT_COLLECTION
    
    log.info(f"Deleting index for field: {field_name}", collection=collection_name)
    
    try:
        client.delete_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            wait=True
        )
        log.info(f"✓ Index deleted successfully for: {field_name}")
        print(f"✓ Index deleted: {field_name}")
        
    except Exception as e:
        log.error(f"Failed to delete index for: {field_name}", error=str(e))
        print(f"❌ Failed to delete index: {field_name}")
        print(f"   Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_existing_indexes()
        elif command == "delete" and len(sys.argv) > 2:
            field_name = sys.argv[2]
            delete_field_index(field_name)
        else:
            print("Usage:")
            print("  python create_indexes.py          # Create all indexes")
            print("  python create_indexes.py list     # List existing indexes")
            print("  python create_indexes.py delete <field>  # Delete specific index")
    else:
        create_field_indexes()
