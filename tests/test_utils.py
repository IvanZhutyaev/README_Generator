"""Tests for utility functions."""

import unittest
import tempfile
import os
from unittest.mock import patch
from generator.utils import (
    print_color, print_success, print_error, print_warning, print_info,
    get_package_dir, find_file, prompt_input, prompt_multiline,
    load_sections_from_string, validate_filename, write_file, read_file,
    ensure_directory, Colors
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_color_functions(self):
        """Test color printing functions (just ensure they don't crash)."""
        with patch('sys.stdout.isatty', return_value=True):
            print_color("test", Colors.GREEN)
            print_success("test")
            print_error("test")
            print_warning("test")
            print_info("test")

    def test_get_package_dir(self):
        """Test getting package directory."""
        pkg_dir = get_package_dir()
        self.assertTrue(os.path.exists(pkg_dir))
        self.assertTrue(pkg_dir.endswith('generator'))

    def test_find_file(self):
        """Test finding file in package."""
        # This might fail if file doesn't exist, but we can test the logic
        result = find_file('nonexistent.txt')
        self.assertIsNone(result)

    @patch('builtins.input')
    def test_prompt_input_with_default(self, mock_input):
        """Test prompt input with default value."""
        mock_input.return_value = ''

        result = prompt_input("Enter value", default="default")
        self.assertEqual(result, "default")

    @patch('builtins.input')
    def test_prompt_input_with_value(self, mock_input):
        """Test prompt input with user value."""
        mock_input.return_value = 'user value'

        result = prompt_input("Enter value", default="default")
        self.assertEqual(result, 'user value')

    @patch('builtins.input')
    def test_prompt_multiline(self, mock_input):
        """Test multiline prompt."""
        mock_input.side_effect = ['line1', 'line2', '']

        result = prompt_multiline("Enter text")
        self.assertEqual(result, 'line1\nline2')

    def test_load_sections_from_string(self):
        """Test loading sections from string."""
        allowed = ['installation', 'usage', 'license']

        result = load_sections_from_string('installation,usage', allowed)
        self.assertEqual(result, ['installation', 'usage'])

        result = load_sections_from_string('installation,invalid', allowed)
        self.assertEqual(result, ['installation'])

        result = load_sections_from_string('', allowed)
        self.assertEqual(result, [])

    def test_validate_filename(self):
        """Test filename validation."""
        self.assertTrue(validate_filename('README.md'))
        self.assertTrue(validate_filename('docs/README.md'))

        self.assertFalse(validate_filename('../README.md'))
        self.assertFalse(validate_filename('/etc/passwd'))
        self.assertFalse(validate_filename('file|name.md'))

    def test_write_and_read_file(self):
        """Test writing and reading files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.txt')
            content = 'test content'

            write_file(filepath, content)
            self.assertTrue(os.path.exists(filepath))

            read_content = read_file(filepath)
            self.assertEqual(read_content, content)

    def test_ensure_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, 'new', 'subdir')

            ensure_directory(new_dir)
            self.assertTrue(os.path.exists(new_dir))


if __name__ == '__main__':
    unittest.main()