import os
from pathlib import Path
from dotenv import load_dotenv

# Try to import logger, but don't fail if it's not available
try:
    from semantic_image_search.backend.logger import GLOBAL_LOGGER as log
    HAS_LOGGER = True
except ImportError as e:
    HAS_LOGGER = False
    print(f"Warning: Could not import logger: {e}")

try:
    from semantic_image_search.backend.exception.custom_exception import SemanticImageSearchException
except ImportError as e:
    print(f"Warning: Could not import custom exception: {e}")
    SemanticImageSearchException = Exception


# Helper function for logging
def safe_log(level, message, **kwargs):
    if HAS_LOGGER:
        getattr(log, level)(message, **kwargs)
    else:
        print(f"[{level.upper()}] {message} {kwargs}")


# ------------------------------------------------------------
# 1) Resolve BASE_DIR
# ------------------------------------------------------------
try:
    BASE_DIR = Path(__file__).resolve().parents[2]
    safe_log("info", "BASE_DIR resolved successfully", base_dir=str(BASE_DIR))
except Exception as e:
    safe_log("error", "Failed to resolve BASE_DIR", error=str(e))
    raise


# ------------------------------------------------------------
# 2) Load .env File
# ------------------------------------------------------------
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(env_path)
    safe_log("info", ".env loaded successfully", env_path=str(env_path))
else:
    safe_log("warning", ".env file not found", env_path=str(env_path))


class Config:
    BASE_DIR: Path = BASE_DIR

    # ------------------- PATHS -------------------
    IMAGES_ROOT: Path = Path(os.getenv("IMAGES_ROOT", BASE_DIR / "images"))
    safe_log("info", "IMAGES_ROOT configured", value=str(IMAGES_ROOT))

    QUERY_IMAGE_ROOT: Path = Path(os.getenv("QUERY_IMAGE_ROOT", BASE_DIR / "data/query_images"))
    safe_log("info", "QUERY_IMAGE_ROOT configured", value=str(QUERY_IMAGE_ROOT))

    RETRIEVED_ROOT: Path = Path(os.getenv("RETRIEVED_ROOT", BASE_DIR / "data/retrieved"))
    safe_log("info", "RETRIEVED_ROOT configured", value=str(RETRIEVED_ROOT))

    # ------------------- CLIP ---------------------
    CLIP_MODEL_NAME: str = os.getenv("CLIP_MODEL_NAME", "ViT-B-32")
    safe_log("info", "CLIP_MODEL_NAME loaded", value=CLIP_MODEL_NAME)

    CLIP_CHECKPOINT: str = os.getenv("CLIP_CHECKPOINT", "laion2b_s34b_b79k")
    safe_log("info", "CLIP_CHECKPOINT loaded", value=CLIP_CHECKPOINT)

    DEVICE: str = os.getenv("DEVICE", "cpu")
    safe_log("info", "DEVICE selected", value=DEVICE)

    # ------------------- QDRANT -------------------
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    if QDRANT_URL:
        safe_log("info", "QDRANT_URL loaded", value=QDRANT_URL)
    else:
        safe_log("warning", "QDRANT_URL missing in environment")

    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    if QDRANT_API_KEY:
        safe_log("info", "QDRANT_API_KEY loaded (hidden)")
    else:
        safe_log("warning", "QDRANT_API_KEY missing in environment")

    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "semantic-image-search")
    safe_log("info", "QDRANT_COLLECTION loaded", value=QDRANT_COLLECTION)

    VECTOR_SIZE: int = int(os.getenv("VECTOR_SIZE", 512))
    safe_log("info", "VECTOR_SIZE loaded", value=VECTOR_SIZE)

    # ------------------- OPENAI -------------------
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    safe_log("info", "OPENAI_MODEL loaded", value=OPENAI_MODEL)

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        safe_log("warning", "OPENAI_API_KEY missing")


# ------------------------------------------------------------
# 7) Final global config success log
# ------------------------------------------------------------
if __name__== "__main__":
    config = Config()
    safe_log("info", "Config initialized successfully", status="OK")
    print(config.VECTOR_SIZE)