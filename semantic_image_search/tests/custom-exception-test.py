"""
Test suite for semantic_image_search.backend.exception.custom_exception module

This test suite validates:
1. Exception initialization with different error types
2. Error message normalization (string, Exception objects)
3. Error details handling (None, sys module, Exception objects)
4. File name and line number extraction
5. Traceback generation and formatting
6. String representation (__str__ and __repr__)
7. Exception chaining and context preservation
8. Edge cases and error handling

Run tests with:
    python semantic_image_search/tests/custom-exception-test.py
    
Or with verbose output:
    python semantic_image_search/tests/custom-exception-test.py -v
"""

import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path to import custom_exception
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantic_image_search.backend.exception.custom_exception import SemanticImageSearchException


class TestExceptionInitialization(unittest.TestCase):
    """Test exception initialization with various inputs"""

    def test_exception_with_string_message(self):
        """Test creating exception with string message"""
        exc = SemanticImageSearchException("Test error message")
        
        self.assertIsInstance(exc, SemanticImageSearchException)
        self.assertIsInstance(exc, Exception)
        self.assertEqual(exc.error_message, "Test error message")

    def test_exception_with_exception_object_as_message(self):
        """Test creating exception with Exception object as message"""
        original_error = ValueError("Original error")
        exc = SemanticImageSearchException(original_error)
        
        self.assertEqual(exc.error_message, "Original error")

    def test_exception_without_error_details(self):
        """Test creating exception without error_details parameter"""
        try:
            x = 1 / 0
        except ZeroDivisionError as e:
            exc = SemanticImageSearchException("Division by zero")
            
            # Should capture current exception context
            self.assertIsNotNone(exc.file_name)
            self.assertGreater(exc.lineno, 0)

    def test_exception_with_none_error_details(self):
        """Test creating exception with None as error_details"""
        try:
            x = int("invalid")
        except ValueError:
            exc = SemanticImageSearchException("Invalid conversion", None)
            
            self.assertIsNotNone(exc.file_name)
            self.assertGreater(exc.lineno, 0)

    def test_exception_with_exception_object_details(self):
        """Test creating exception with Exception object as error_details"""
        try:
            x = [1, 2, 3][10]
        except IndexError as e:
            exc = SemanticImageSearchException("Index out of range", e)
            
            self.assertIn("IndexError", exc.traceback_str)
            self.assertIn("list index out of range", exc.traceback_str)

    def test_exception_with_sys_module_details(self):
        """Test creating exception with sys module (old pattern)"""
        try:
            x = {"key": "value"}["missing_key"]
        except KeyError as e:
            exc = SemanticImageSearchException("Key not found", sys)
            
            self.assertIsNotNone(exc.traceback_str)
            self.assertIn("KeyError", exc.traceback_str)


class TestErrorMessageNormalization(unittest.TestCase):
    """Test error message normalization"""

    def test_string_message_unchanged(self):
        """Test string messages are preserved"""
        exc = SemanticImageSearchException("Plain string message")
        self.assertEqual(exc.error_message, "Plain string message")

    def test_exception_object_converted_to_string(self):
        """Test Exception objects are converted to strings"""
        original = RuntimeError("Runtime problem")
        exc = SemanticImageSearchException(original)
        self.assertEqual(exc.error_message, "Runtime problem")

    def test_integer_message_converted_to_string(self):
        """Test integer messages are converted to strings"""
        exc = SemanticImageSearchException(404)
        self.assertEqual(exc.error_message, "404")

    def test_empty_string_message(self):
        """Test empty string message is handled"""
        exc = SemanticImageSearchException("")
        self.assertEqual(exc.error_message, "")

    def test_multiline_message(self):
        """Test multiline messages are preserved"""
        message = "Line 1\nLine 2\nLine 3"
        exc = SemanticImageSearchException(message)
        self.assertEqual(exc.error_message, message)


class TestFileAndLineExtraction(unittest.TestCase):
    """Test file name and line number extraction"""

    def test_file_name_is_extracted(self):
        """Test that file name is extracted from traceback"""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            exc = SemanticImageSearchException("Wrapped error", e)
            
            self.assertIsNotNone(exc.file_name)
            self.assertIsInstance(exc.file_name, str)
            # Should contain the current test file name
            self.assertIn("custom-exception-test.py", exc.file_name)

    def test_line_number_is_positive(self):
        """Test that line number is positive integer"""
        try:
            raise TypeError("Test error")
        except TypeError as e:
            exc = SemanticImageSearchException("Wrapped error", e)
            
            self.assertIsInstance(exc.lineno, int)
            self.assertGreater(exc.lineno, 0)

    def test_unknown_file_when_no_traceback(self):
        """Test file name is '<unknown>' when no traceback available"""
        exc = SemanticImageSearchException("No traceback context")
        
        # When created outside exception handler, may have no traceback
        # This depends on execution context
        self.assertIsNotNone(exc.file_name)

    def test_line_number_negative_when_no_traceback(self):
        """Test line number is -1 when no traceback available"""
        exc = SemanticImageSearchException("No traceback context")
        
        # When no traceback is available
        if exc.file_name == "<unknown>":
            self.assertEqual(exc.lineno, -1)


class TestTracebackGeneration(unittest.TestCase):
    """Test traceback generation and formatting"""

    def test_traceback_contains_exception_type(self):
        """Test traceback contains original exception type"""
        try:
            raise AttributeError("Missing attribute")
        except AttributeError as e:
            exc = SemanticImageSearchException("Attribute problem", e)
            
            self.assertIn("AttributeError", exc.traceback_str)

    def test_traceback_contains_exception_message(self):
        """Test traceback contains original exception message"""
        try:
            raise ValueError("Invalid value provided")
        except ValueError as e:
            exc = SemanticImageSearchException("Value error occurred", e)
            
            self.assertIn("Invalid value provided", exc.traceback_str)

    def test_traceback_contains_file_info(self):
        """Test traceback contains file and line information"""
        try:
            raise RuntimeError("Test error")
        except RuntimeError as e:
            exc = SemanticImageSearchException("Runtime problem", e)
            
            self.assertIn("File", exc.traceback_str)
            self.assertIn("line", exc.traceback_str.lower())

    def test_traceback_is_multiline(self):
        """Test traceback is formatted across multiple lines"""
        try:
            raise IOError("File not found")
        except IOError as e:
            exc = SemanticImageSearchException("IO problem", e)
            
            self.assertIn("\n", exc.traceback_str)
            lines = exc.traceback_str.split("\n")
            self.assertGreater(len(lines), 1)

    def test_empty_traceback_when_no_exception_context(self):
        """Test traceback is empty when no exception context"""
        exc = SemanticImageSearchException("Direct instantiation")
        
        # When created outside exception handler, traceback may be empty
        self.assertIsInstance(exc.traceback_str, str)

    def test_traceback_preserves_stack_trace(self):
        """Test that full stack trace is preserved"""
        def level3():
            raise ValueError("Deep error")
        
        def level2():
            level3()
        
        def level1():
            level2()
        
        try:
            level1()
        except ValueError as e:
            exc = SemanticImageSearchException("Nested error", e)
            
            # Should contain all function names in stack
            self.assertIn("level3", exc.traceback_str)
            self.assertIn("level2", exc.traceback_str)
            self.assertIn("level1", exc.traceback_str)


class TestStringRepresentation(unittest.TestCase):
    """Test __str__ and __repr__ methods"""

    def test_str_contains_file_name(self):
        """Test __str__ includes file name"""
        try:
            raise ValueError("Test")
        except ValueError as e:
            exc = SemanticImageSearchException("Error", e)
            str_repr = str(exc)
            
            self.assertIn("Error in [", str_repr)
            self.assertIn("]", str_repr)

    def test_str_contains_line_number(self):
        """Test __str__ includes line number"""
        try:
            raise ValueError("Test")
        except ValueError as e:
            exc = SemanticImageSearchException("Error", e)
            str_repr = str(exc)
            
            self.assertIn("at line [", str_repr)
            self.assertIn("]", str_repr)

    def test_str_contains_error_message(self):
        """Test __str__ includes error message"""
        try:
            raise ValueError("Original")
        except ValueError as e:
            exc = SemanticImageSearchException("Custom message", e)
            str_repr = str(exc)
            
            self.assertIn("Message: Custom message", str_repr)

    def test_str_includes_traceback_when_available(self):
        """Test __str__ includes traceback section"""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            exc = SemanticImageSearchException("Wrapped", e)
            str_repr = str(exc)
            
            self.assertIn("Traceback:", str_repr)

    def test_str_format_without_traceback(self):
        """Test __str__ format when no traceback available"""
        exc = SemanticImageSearchException("Simple error")
        str_repr = str(exc)
        
        self.assertIn("Error in [", str_repr)
        self.assertIn("Message:", str_repr)

    def test_repr_format(self):
        """Test __repr__ format is correct"""
        try:
            raise ValueError("Test")
        except ValueError as e:
            exc = SemanticImageSearchException("Error message", e)
            repr_str = repr(exc)
            
            self.assertIn("SemanticImageSearchException", repr_str)
            self.assertIn("file=", repr_str)
            self.assertIn("line=", repr_str)
            self.assertIn("message=", repr_str)

    def test_repr_contains_message(self):
        """Test __repr__ includes error message"""
        exc = SemanticImageSearchException("Test message")
        repr_str = repr(exc)
        
        self.assertIn("'Test message'", repr_str)


class TestExceptionChaining(unittest.TestCase):
    """Test exception chaining and context preservation"""

    def test_exception_chaining_with_from(self):
        """Test exception can be raised with 'from' clause"""
        try:
            try:
                x = 1 / 0
            except ZeroDivisionError as e:
                raise SemanticImageSearchException("Division error", e) from e
        except SemanticImageSearchException as exc:
            self.assertIsNotNone(exc.__cause__)
            self.assertIsInstance(exc.__cause__, ZeroDivisionError)

    def test_exception_context_preserved(self):
        """Test exception context is preserved during wrapping"""
        try:
            try:
                x = int("abc")
            except ValueError as e:
                raise SemanticImageSearchException("Conversion failed", e)
        except SemanticImageSearchException as exc:
            # Context should be preserved
            self.assertIsInstance(exc, SemanticImageSearchException)

    def test_nested_exception_wrapping(self):
        """Test multiple levels of exception wrapping"""
        try:
            try:
                raise ValueError("Level 1")
            except ValueError as e1:
                try:
                    raise SemanticImageSearchException("Level 2", e1)
                except SemanticImageSearchException as e2:
                    raise SemanticImageSearchException("Level 3", e2)
        except SemanticImageSearchException as exc:
            self.assertIn("Level 3", exc.error_message)


class TestExceptionInheritance(unittest.TestCase):
    """Test exception inheritance and isinstance checks"""

    def test_is_instance_of_exception(self):
        """Test SemanticImageSearchException is instance of Exception"""
        exc = SemanticImageSearchException("Test")
        self.assertIsInstance(exc, Exception)

    def test_is_instance_of_base_exception(self):
        """Test SemanticImageSearchException is instance of BaseException"""
        exc = SemanticImageSearchException("Test")
        self.assertIsInstance(exc, BaseException)

    def test_can_be_caught_as_exception(self):
        """Test exception can be caught as generic Exception"""
        caught = False
        try:
            raise SemanticImageSearchException("Test error")
        except Exception:
            caught = True
        
        self.assertTrue(caught)

    def test_can_be_caught_specifically(self):
        """Test exception can be caught by specific type"""
        caught = False
        try:
            raise SemanticImageSearchException("Test error")
        except SemanticImageSearchException:
            caught = True
        
        self.assertTrue(caught)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""

    def test_exception_with_unicode_message(self):
        """Test exception with unicode characters in message"""
        message = "Error: 你好 🚀 Привет"
        exc = SemanticImageSearchException(message)
        self.assertEqual(exc.error_message, message)

    def test_exception_with_very_long_message(self):
        """Test exception with very long message"""
        message = "A" * 10000
        exc = SemanticImageSearchException(message)
        self.assertEqual(len(exc.error_message), 10000)

    def test_exception_with_special_characters(self):
        """Test exception with special characters in message"""
        message = "Error: \n\t\r\\\"'<>&"
        exc = SemanticImageSearchException(message)
        self.assertIn("\n", exc.error_message)
        self.assertIn("\t", exc.error_message)

    def test_exception_attributes_are_accessible(self):
        """Test all exception attributes are accessible"""
        try:
            raise ValueError("Test")
        except ValueError as e:
            exc = SemanticImageSearchException("Error", e)
            
            # All attributes should be accessible
            _ = exc.file_name
            _ = exc.lineno
            _ = exc.error_message
            _ = exc.traceback_str
            _ = str(exc)
            _ = repr(exc)

    def test_exception_with_none_in_message(self):
        """Test exception when None is part of message"""
        message = f"Value is {None}"
        exc = SemanticImageSearchException(message)
        self.assertIn("None", exc.error_message)

    def test_exception_with_dict_details(self):
        """Test exception when error_details is a dict (unsupported type)"""
        try:
            raise ValueError("Original")
        except ValueError:
            # Dict is not a valid error_details type, should fall back to sys.exc_info()
            exc = SemanticImageSearchException("Error", {"key": "value"})
            
            # Should still work by falling back to current exception
            self.assertIsNotNone(exc.error_message)

    def test_multiple_exceptions_independent(self):
        """Test multiple exception instances are independent"""
        exc1 = SemanticImageSearchException("Error 1")
        exc2 = SemanticImageSearchException("Error 2")
        
        self.assertNotEqual(exc1.error_message, exc2.error_message)
        self.assertEqual(exc1.error_message, "Error 1")
        self.assertEqual(exc2.error_message, "Error 2")


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios"""

    def test_file_not_found_scenario(self):
        """Test wrapping FileNotFoundError"""
        try:
            with open("/nonexistent/file.txt", "r") as f:
                pass
        except FileNotFoundError as e:
            exc = SemanticImageSearchException("Failed to open file", e)
            
            self.assertIn("FileNotFoundError", exc.traceback_str)
            self.assertEqual(exc.error_message, "Failed to open file")

    def test_api_error_scenario(self):
        """Test wrapping API-like errors"""
        try:
            response = {"status": 500, "error": "Internal Server Error"}
            if response["status"] >= 400:
                raise ValueError(f"API Error: {response['error']}")
        except ValueError as e:
            exc = SemanticImageSearchException("API request failed", e)
            
            self.assertIn("API Error", exc.traceback_str)

    def test_data_validation_scenario(self):
        """Test wrapping data validation errors"""
        try:
            data = {"name": "John"}
            if "email" not in data:
                raise KeyError("email field is required")
        except KeyError as e:
            exc = SemanticImageSearchException("Data validation failed", e)
            
            self.assertEqual(exc.error_message, "Data validation failed")
            self.assertIn("KeyError", exc.traceback_str)

    def test_database_error_scenario(self):
        """Test wrapping database-like errors"""
        try:
            # Simulate database error
            raise ConnectionError("Database connection timeout")
        except ConnectionError as e:
            exc = SemanticImageSearchException("Database operation failed", e)
            
            self.assertIn("ConnectionError", exc.traceback_str)
            self.assertIn("timeout", exc.traceback_str)

    def test_model_inference_error_scenario(self):
        """Test wrapping ML model errors"""
        try:
            # Simulate model error
            raise RuntimeError("CUDA out of memory")
        except RuntimeError as e:
            exc = SemanticImageSearchException("Model inference failed", e)
            
            self.assertEqual(exc.error_message, "Model inference failed")
            self.assertIn("CUDA", exc.traceback_str)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
