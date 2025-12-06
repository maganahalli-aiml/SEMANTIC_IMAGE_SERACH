"""
Test suite for semantic_image_search.backend.logger.custom_logger module

This test suite validates:
1. CustomLogger initialization and directory creation
2. Log file creation with proper naming
3. Logger instance creation and configuration
4. JSON structured logging functionality
5. Multiple log levels (info, warning, error)
6. File and console handlers
7. Structlog configuration

Run tests with:
    python semantic_image_search/tests/custom-logger-test.py
    
Or with verbose output:
    python semantic_image_search/tests/custom-logger-test.py -v
"""

import os
import sys
import json
import logging
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from io import StringIO
from unittest.mock import patch, MagicMock

# Add parent directory to path to import custom_logger
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantic_image_search.backend.logger.custom_logger import CustomLogger


class TestCustomLoggerInitialization(unittest.TestCase):
    """Test CustomLogger initialization and directory creation"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_logger_initialization_default_dir(self):
        """Test CustomLogger creates logs directory by default"""
        logger_instance = CustomLogger()
        
        self.assertTrue(os.path.exists(logger_instance.logs_dir))
        self.assertTrue(os.path.isdir(logger_instance.logs_dir))
        self.assertTrue(logger_instance.logs_dir.endswith("logs"))

    def test_logger_initialization_custom_dir(self):
        """Test CustomLogger creates custom log directory"""
        custom_dir = "custom_logs"
        logger_instance = CustomLogger(log_dir=custom_dir)
        
        self.assertTrue(os.path.exists(logger_instance.logs_dir))
        self.assertTrue(logger_instance.logs_dir.endswith(custom_dir))

    def test_log_file_path_creation(self):
        """Test log file path is created with timestamp"""
        logger_instance = CustomLogger()
        
        self.assertIsNotNone(logger_instance.log_file_path)
        self.assertTrue(logger_instance.log_file_path.endswith('.log'))
        
        # Check timestamp format in filename
        filename = os.path.basename(logger_instance.log_file_path)
        self.assertRegex(filename, r'\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2}\.log')

    def test_logs_dir_attribute(self):
        """Test logs_dir attribute is set correctly"""
        logger_instance = CustomLogger()
        
        expected_dir = os.path.join(os.getcwd(), "logs")
        self.assertEqual(logger_instance.logs_dir, expected_dir)

    def test_multiple_logger_instances(self):
        """Test multiple CustomLogger instances create separate log files"""
        logger1 = CustomLogger()
        import time
        time.sleep(1)  # Ensure different timestamp
        logger2 = CustomLogger()
        
        self.assertNotEqual(logger1.log_file_path, logger2.log_file_path)

    def test_logs_directory_already_exists(self):
        """Test CustomLogger works when logs directory already exists"""
        os.makedirs("logs", exist_ok=True)
        
        # Should not raise an error
        logger_instance = CustomLogger()
        self.assertTrue(os.path.exists(logger_instance.logs_dir))


class TestLoggerInstance(unittest.TestCase):
    """Test logger instance creation and configuration"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.logger_instance = CustomLogger()

    def tearDown(self):
        """Clean up temporary directory and reset logging"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Close and clear logging handlers
        for handler in logging.getLogger().handlers[:]:
            handler.close()
            logging.getLogger().removeHandler(handler)
        logging.getLogger().handlers.clear()

    def test_get_logger_returns_logger_object(self):
        """Test get_logger returns a logger object"""
        logger = self.logger_instance.get_logger("test_logger")
        
        self.assertIsNotNone(logger)
        # Check it has logging methods
        self.assertTrue(hasattr(logger, 'info'))
        self.assertTrue(hasattr(logger, 'warning'))
        self.assertTrue(hasattr(logger, 'error'))
        self.assertTrue(hasattr(logger, 'debug'))

    def test_get_logger_with_custom_name(self):
        """Test get_logger with custom logger name"""
        logger = self.logger_instance.get_logger("custom_app")
        
        self.assertIsNotNone(logger)

    def test_get_logger_with_file_path(self):
        """Test get_logger extracts basename from file path"""
        logger = self.logger_instance.get_logger("/path/to/module.py")
        
        self.assertIsNotNone(logger)

    def test_get_logger_default_name(self):
        """Test get_logger with default __file__ name"""
        logger = self.logger_instance.get_logger()
        
        self.assertIsNotNone(logger)


class TestLoggingFunctionality(unittest.TestCase):
    """Test actual logging functionality"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.logger_instance = CustomLogger()
        self.logger = self.logger_instance.get_logger("test_app")

    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Close and clear logging handlers
        for handler in logging.getLogger().handlers[:]:
            handler.close()
            logging.getLogger().removeHandler(handler)
        logging.getLogger().handlers.clear()

    def test_info_logging_to_file(self):
        """Test info level logging writes to file"""
        test_message = "Test info message"
        self.logger.info(test_message, user_id=123)
        
        # Read log file
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn(test_message, log_content)
        self.assertIn('"level": "info"', log_content)
        self.assertIn('"user_id": 123', log_content)

    def test_error_logging_to_file(self):
        """Test error level logging writes to file"""
        test_message = "Test error message"
        self.logger.error(test_message, error_code=500)
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn(test_message, log_content)
        self.assertIn('"level": "error"', log_content)
        self.assertIn('"error_code": 500', log_content)

    def test_warning_logging_to_file(self):
        """Test warning level logging writes to file"""
        test_message = "Test warning message"
        self.logger.warning(test_message, status="deprecated")
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn(test_message, log_content)
        self.assertIn('"level": "warning"', log_content)
        self.assertIn('"status": "deprecated"', log_content)

    def test_json_format_logging(self):
        """Test logs are in valid JSON format"""
        self.logger.info("JSON test", key="value", number=42)
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_lines = f.readlines()
        
        # Each line should be valid JSON
        for line in log_lines:
            try:
                log_entry = json.loads(line.strip())
                self.assertIsInstance(log_entry, dict)
                self.assertIn('event', log_entry)
                self.assertIn('level', log_entry)
                self.assertIn('timestamp', log_entry)
            except json.JSONDecodeError:
                self.fail(f"Log line is not valid JSON: {line}")

    def test_logging_with_multiple_fields(self):
        """Test logging with multiple custom fields"""
        self.logger.info(
            "Multiple fields test",
            user_id=123,
            action="upload",
            filename="test.pdf",
            size=1024
        )
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn('"user_id": 123', log_content)
        self.assertIn('"action": "upload"', log_content)
        self.assertIn('"filename": "test.pdf"', log_content)
        self.assertIn('"size": 1024', log_content)

    def test_timestamp_in_iso_format(self):
        """Test timestamp is in ISO format with UTC"""
        self.logger.info("Timestamp test")
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_line = f.readline()
        
        log_entry = json.loads(log_line.strip())
        
        self.assertIn('timestamp', log_entry)
        # Check ISO format with Z for UTC
        self.assertRegex(
            log_entry['timestamp'],
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z'
        )

    def test_event_field_renamed(self):
        """Test that message is renamed to 'event' in logs"""
        self.logger.info("Test event message")
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_line = f.readline()
        
        log_entry = json.loads(log_line.strip())
        
        self.assertIn('event', log_entry)
        self.assertEqual(log_entry['event'], "Test event message")
        self.assertNotIn('message', log_entry)

    def test_multiple_log_entries(self):
        """Test multiple log entries are written correctly"""
        messages = ["First message", "Second message", "Third message"]
        
        for msg in messages:
            self.logger.info(msg)
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_lines = f.readlines()
        
        self.assertEqual(len(log_lines), len(messages))
        
        for i, line in enumerate(log_lines):
            log_entry = json.loads(line.strip())
            self.assertEqual(log_entry['event'], messages[i])

    def test_logging_with_special_characters(self):
        """Test logging with special characters is properly escaped"""
        special_message = 'Test with "quotes" and \n newlines'
        self.logger.info(special_message)
        
        with open(self.logger_instance.log_file_path, 'r') as f:
            log_line = f.readline()
        
        # Should be valid JSON even with special characters
        log_entry = json.loads(log_line.strip())
        self.assertIn('quotes', log_entry['event'])


class TestConsoleLogging(unittest.TestCase):
    """Test console (stderr) logging functionality"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.logger_instance = CustomLogger()

    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Close and clear logging handlers
        for handler in logging.getLogger().handlers[:]:
            handler.close()
            logging.getLogger().removeHandler(handler)
        logging.getLogger().handlers.clear()

    def test_console_output(self):
        """Test that logs are also written to console"""
        # Create a StringIO to capture console output
        console_stream = StringIO()
        
        # Get logger and replace stderr handler's stream
        logger = self.logger_instance.get_logger("console_test")
        
        # Find and replace the console handler's stream
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.stream = console_stream
        
        # Log a message
        logger.info("Console test message")
        
        # Check that it was written
        console_output = console_stream.getvalue()
        self.assertIn("Console test message", console_output)
        self.assertIn('"level": "info"', console_output)
        
        console_stream.close()


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Close and clear logging handlers
        for handler in logging.getLogger().handlers[:]:
            handler.close()
            logging.getLogger().removeHandler(handler)
        logging.getLogger().handlers.clear()

    def test_empty_log_message(self):
        """Test logging with empty message"""
        logger_instance = CustomLogger()
        logger = logger_instance.get_logger("test")
        
        logger.info("")
        
        with open(logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn('"event": ""', log_content)

    def test_logging_with_none_values(self):
        """Test logging with None values"""
        logger_instance = CustomLogger()
        logger = logger_instance.get_logger("test")
        
        logger.info("None value test", value=None)
        
        with open(logger_instance.log_file_path, 'r') as f:
            log_line = f.readline()
        
        log_entry = json.loads(log_line.strip())
        self.assertIn('value', log_entry)
        self.assertIsNone(log_entry['value'])

    def test_logging_with_boolean_values(self):
        """Test logging with boolean values"""
        logger_instance = CustomLogger()
        logger = logger_instance.get_logger("test")
        
        logger.info("Boolean test", success=True, failed=False)
        
        with open(logger_instance.log_file_path, 'r') as f:
            log_content = f.read()
        
        self.assertIn('"success": true', log_content)
        self.assertIn('"failed": false', log_content)

    def test_logging_with_nested_dict(self):
        """Test logging with nested dictionary values"""
        logger_instance = CustomLogger()
        logger = logger_instance.get_logger("test")
        
        nested_data = {"user": {"id": 123, "name": "test"}}
        logger.info("Nested data test", data=nested_data)
        
        with open(logger_instance.log_file_path, 'r') as f:
            log_line = f.readline()
        
        log_entry = json.loads(log_line.strip())
        self.assertIn('data', log_entry)
        self.assertEqual(log_entry['data']['user']['id'], 123)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
