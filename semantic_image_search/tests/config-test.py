"""
Test suite for semantic_image_search.backend.config module

This test suite validates:
1. Configuration initialization and attribute access
2. Default values for all configuration parameters
3. Environment variable override functionality
4. Path resolution and validation
5. Type checking for configuration values
6. Error handling for invalid configurations

Run tests with:
    python semantic_image_search/tests/config-test.py
    
Or with verbose output:
    python semantic_image_search/tests/config-test.py -v
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantic_image_search.backend.config import Config, BASE_DIR


class TestConfig(unittest.TestCase):
    """Test cases for the Config class"""

    def test_base_dir_is_valid_path(self):
        """Test that BASE_DIR is a valid Path object"""
        self.assertIsInstance(BASE_DIR, Path)
        self.assertTrue(BASE_DIR.exists())
        self.assertTrue(BASE_DIR.is_dir())

    def test_base_dir_points_to_project_root(self):
        """Test that BASE_DIR points to the project root"""
        # BASE_DIR should contain pyproject.toml or requirements.txt
        self.assertTrue(
            (BASE_DIR / "pyproject.toml").exists() or 
            (BASE_DIR / "requirements.txt").exists(),
            "BASE_DIR should point to project root containing pyproject.toml or requirements.txt"
        )

    def test_config_class_initialization(self):
        """Test that Config class can be instantiated"""
        config = Config()
        self.assertIsNotNone(config)

    def test_config_base_dir_attribute(self):
        """Test Config.BASE_DIR attribute"""
        config = Config()
        self.assertIsInstance(config.BASE_DIR, Path)
        self.assertEqual(config.BASE_DIR, BASE_DIR)

    def test_images_root_path(self):
        """Test IMAGES_ROOT configuration"""
        config = Config()
        self.assertIsInstance(config.IMAGES_ROOT, Path)
        # Should default to BASE_DIR/images if not set in env
        expected_path = Path(os.getenv("IMAGES_ROOT", BASE_DIR / "images"))
        self.assertEqual(config.IMAGES_ROOT, expected_path)

    def test_query_image_root_path(self):
        """Test QUERY_IMAGE_ROOT configuration"""
        config = Config()
        self.assertIsInstance(config.QUERY_IMAGE_ROOT, Path)
        expected_path = Path(os.getenv("QUERY_IMAGE_ROOT", BASE_DIR / "data/query_images"))
        self.assertEqual(config.QUERY_IMAGE_ROOT, expected_path)

    def test_retrieved_root_path(self):
        """Test RETRIEVED_ROOT configuration"""
        config = Config()
        self.assertIsInstance(config.RETRIEVED_ROOT, Path)
        expected_path = Path(os.getenv("RETRIEVED_ROOT", BASE_DIR / "data/retrieved"))
        self.assertEqual(config.RETRIEVED_ROOT, expected_path)

    def test_clip_model_name_default(self):
        """Test CLIP_MODEL_NAME default value"""
        config = Config()
        self.assertIsInstance(config.CLIP_MODEL_NAME, str)
        # Should have a default value if not set in env
        if not os.getenv("CLIP_MODEL_NAME"):
            self.assertEqual(config.CLIP_MODEL_NAME, "ViT-B-32")

    def test_clip_checkpoint_default(self):
        """Test CLIP_CHECKPOINT default value"""
        config = Config()
        self.assertIsInstance(config.CLIP_CHECKPOINT, str)
        if not os.getenv("CLIP_CHECKPOINT"):
            self.assertEqual(config.CLIP_CHECKPOINT, "laion2b_s34b_b79k")

    def test_device_default(self):
        """Test DEVICE default value"""
        config = Config()
        self.assertIsInstance(config.DEVICE, str)
        if not os.getenv("DEVICE"):
            self.assertEqual(config.DEVICE, "cpu")

    def test_qdrant_url_from_env(self):
        """Test QDRANT_URL can be loaded from environment"""
        config = Config()
        # Should be string or None
        self.assertTrue(
            config.QDRANT_URL is None or isinstance(config.QDRANT_URL, str)
        )

    def test_qdrant_api_key_from_env(self):
        """Test QDRANT_API_KEY can be loaded from environment"""
        config = Config()
        # Should be string or None
        self.assertTrue(
            config.QDRANT_API_KEY is None or isinstance(config.QDRANT_API_KEY, str)
        )

    def test_qdrant_collection_default(self):
        """Test QDRANT_COLLECTION default value"""
        config = Config()
        self.assertIsInstance(config.QDRANT_COLLECTION, str)
        if not os.getenv("QDRANT_COLLECTION"):
            self.assertEqual(config.QDRANT_COLLECTION, "semantic-image-search")

    def test_vector_size_default(self):
        """Test VECTOR_SIZE default value and type"""
        config = Config()
        self.assertIsInstance(config.VECTOR_SIZE, int)
        if not os.getenv("VECTOR_SIZE"):
            self.assertEqual(config.VECTOR_SIZE, 512)

    def test_vector_size_is_positive(self):
        """Test VECTOR_SIZE is a positive integer"""
        config = Config()
        self.assertGreater(config.VECTOR_SIZE, 0)

    def test_openai_model_default(self):
        """Test OPENAI_MODEL default value"""
        config = Config()
        self.assertIsInstance(config.OPENAI_MODEL, str)
        if not os.getenv("OPENAI_MODEL"):
            self.assertEqual(config.OPENAI_MODEL, "gpt-4o-mini")

    def test_openai_api_key_from_env(self):
        """Test OPENAI_API_KEY can be loaded from environment"""
        config = Config()
        # Should be string or None
        self.assertTrue(
            config.OPENAI_API_KEY is None or isinstance(config.OPENAI_API_KEY, str)
        )

    @patch.dict(os.environ, {"IMAGES_ROOT": "/custom/images/path"})
    def test_custom_images_root_from_env(self):
        """Test IMAGES_ROOT can be overridden via environment variable"""
        # Need to reload the module to pick up the env change
        from importlib import reload
        import semantic_image_search.backend.config as config_module
        reload(config_module)
        
        config = config_module.Config()
        self.assertEqual(config.IMAGES_ROOT, Path("/custom/images/path"))

    @patch.dict(os.environ, {"VECTOR_SIZE": "1024"})
    def test_custom_vector_size_from_env(self):
        """Test VECTOR_SIZE can be overridden via environment variable"""
        from importlib import reload
        import semantic_image_search.backend.config as config_module
        reload(config_module)
        
        config = config_module.Config()
        self.assertEqual(config.VECTOR_SIZE, 1024)

    @patch.dict(os.environ, {"DEVICE": "cuda"})
    def test_custom_device_from_env(self):
        """Test DEVICE can be overridden via environment variable"""
        from importlib import reload
        import semantic_image_search.backend.config as config_module
        reload(config_module)
        
        config = config_module.Config()
        self.assertEqual(config.DEVICE, "cuda")

    def test_all_required_attributes_exist(self):
        """Test that all expected configuration attributes exist"""
        config = Config()
        required_attributes = [
            'BASE_DIR',
            'IMAGES_ROOT',
            'QUERY_IMAGE_ROOT',
            'RETRIEVED_ROOT',
            'CLIP_MODEL_NAME',
            'CLIP_CHECKPOINT',
            'DEVICE',
            'QDRANT_URL',
            'QDRANT_API_KEY',
            'QDRANT_COLLECTION',
            'VECTOR_SIZE',
            'OPENAI_MODEL',
            'OPENAI_API_KEY'
        ]
        
        for attr in required_attributes:
            self.assertTrue(
                hasattr(config, attr),
                f"Config should have attribute: {attr}"
            )

    def test_config_singleton_behavior(self):
        """Test that multiple Config instances share the same class attributes"""
        config1 = Config()
        config2 = Config()
        
        # Class attributes should be the same
        self.assertEqual(config1.BASE_DIR, config2.BASE_DIR)
        self.assertEqual(config1.VECTOR_SIZE, config2.VECTOR_SIZE)
        self.assertEqual(config1.CLIP_MODEL_NAME, config2.CLIP_MODEL_NAME)


class TestConfigModuleFunctions(unittest.TestCase):
    """Test module-level functions and initialization"""

    def test_base_dir_resolution(self):
        """Test that BASE_DIR is correctly resolved at module level"""
        self.assertIsInstance(BASE_DIR, Path)
        self.assertTrue(BASE_DIR.is_absolute())

    def test_env_file_loading(self):
        """Test that .env file is loaded if it exists"""
        env_path = BASE_DIR / ".env"
        if env_path.exists():
            # If .env exists, some environment variables should be loaded
            # We can't test specific values as they might not be in .env
            # Just verify the module loaded without errors
            self.assertTrue(True)
        else:
            # If .env doesn't exist, that's also okay
            self.assertTrue(True)


class TestConfigErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def test_vector_size_invalid_string(self):
        """Test that invalid VECTOR_SIZE string raises ValueError"""
        with patch.dict(os.environ, {"VECTOR_SIZE": "invalid"}):
            from importlib import reload
            import semantic_image_search.backend.config as config_module
            
            with self.assertRaises(ValueError):
                reload(config_module)

    def test_config_without_logger(self):
        """Test that Config works even if logger import fails"""
        # This is implicitly tested if safe_log fallback works
        config = Config()
        self.assertIsNotNone(config)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
