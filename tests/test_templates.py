"""Tests for templates module."""

import unittest
import tempfile
import os
from unittest.mock import patch
from generator.templates import (
    list_templates, get_template, save_template,
    validate_template, TemplateNotFoundError, TemplateError,
    DEFAULT_TEMPLATE, TEMPLATE_DIR
)


class TestTemplates(unittest.TestCase):
    """Test cases for template functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.patcher = patch('generator.templates.TEMPLATE_DIR', self.temp_dir.name)
        self.patcher.start()

    def tearDown(self):
        """Clean up test fixtures."""
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_list_templates_empty(self):
        """Test listing templates when directory is empty."""
        templates = list_templates()
        self.assertEqual(templates, [])

    def test_list_templates_with_files(self):
        """Test listing templates with files."""
        # Create some template files
        with open(os.path.join(self.temp_dir.name, 'default.md'), 'w') as f:
            f.write('test')
        with open(os.path.join(self.temp_dir.name, 'python.md'), 'w') as f:
            f.write('test')
        with open(os.path.join(self.temp_dir.name, 'default_ru.md'), 'w') as f:
            f.write('test')

        templates = list_templates()
        self.assertIn('default', templates)
        self.assertIn('python', templates)
        self.assertEqual(len(templates), 2)

    def test_save_and_get_template(self):
        """Test saving and retrieving a template."""
        content = '# {title}\n\n{description}'
        saved_path = save_template('test', content)

        self.assertTrue(os.path.exists(saved_path))

        retrieved = get_template('test')
        self.assertEqual(retrieved, content)

    def test_get_template_with_lang(self):
        """Test getting template with language variant."""
        content_en = '# English'
        content_ru = '# Русский'

        save_template('test', content_en, 'en')
        save_template('test', content_ru, 'ru')

        self.assertEqual(get_template('test', 'en'), content_en)
        self.assertEqual(get_template('test', 'ru'), content_ru)

    def test_get_template_not_found(self):
        """Test getting non-existent template raises error."""
        with self.assertRaises(TemplateNotFoundError):
            get_template('nonexistent')

    def test_validate_template_valid(self):
        """Test validation of valid template."""
        content = '# {title}\n\n{description}\n\n{installation}'
        self.assertTrue(validate_template(content))

    def test_validate_template_invalid(self):
        """Test validation of invalid template."""
        content = '# No placeholders'
        self.assertFalse(validate_template(content))

    def test_default_template_fallback(self):
        """Test that DEFAULT_TEMPLATE is used when no template found."""
        from generator.templates import DEFAULT_TEMPLATE
        self.assertIn('{title}', DEFAULT_TEMPLATE)
        self.assertIn('{description}', DEFAULT_TEMPLATE)


if __name__ == '__main__':
    unittest.main()