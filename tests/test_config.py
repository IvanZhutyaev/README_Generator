"""Tests for configuration module."""

import unittest
import tempfile
import json
import os
from generator.config import (
    load_config, save_config, merge_with_defaults,
    validate_config, ConfigNotFoundError, ConfigInvalidError,
    DEFAULT_CONFIG, get_config_path
)


class TestConfig(unittest.TestCase):
    """Test cases for configuration functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'config.json')

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        data = {
            'title': 'Test Project',
            'lang': 'ru',
            'sections': ['installation', 'usage']
        }

        save_config(self.config_path, data)
        loaded = load_config(self.config_path)

        self.assertEqual(loaded, data)

    def test_load_config_not_found(self):
        """Test loading non-existent config raises error."""
        with self.assertRaises(ConfigNotFoundError):
            load_config('nonexistent.json')

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises error."""
        with open(self.config_path, 'w') as f:
            f.write('{invalid json}')

        with self.assertRaises(ConfigInvalidError):
            load_config(self.config_path)

    def test_merge_with_defaults(self):
        """Test merging user config with defaults."""
        user = {'title': 'Test', 'sections': 'installation,usage'}
        merged = merge_with_defaults(user)

        self.assertEqual(merged['title'], 'Test')
        self.assertEqual(merged['lang'], 'en')
        self.assertEqual(merged['output'], 'README.md')
        self.assertEqual(merged['template'], 'default')
        self.assertEqual(merged['sections'], ['installation', 'usage'])

    def test_merge_with_defaults_list_sections(self):
        """Test merging when sections is a list."""
        user = {'title': 'Test', 'sections': ['installation', 'usage']}
        merged = merge_with_defaults(user)

        self.assertEqual(merged['sections'], ['installation', 'usage'])

    def test_validate_config_valid(self):
        """Test validation of valid config."""
        config = DEFAULT_CONFIG.copy()
        config['title'] = 'Test'
        config['sections'] = ['installation']

        self.assertTrue(validate_config(config))

    def test_validate_config_invalid_lang(self):
        """Test validation with invalid language."""
        config = DEFAULT_CONFIG.copy()
        config['lang'] = 'fr'

        self.assertFalse(validate_config(config))

    def test_validate_config_missing_keys(self):
        """Test validation with missing keys."""
        config = {}
        self.assertFalse(validate_config(config))

    def test_get_config_path(self):
        """Test getting config path."""
        path = get_config_path('test.json')
        self.assertTrue(path.endswith('test.json'))
        self.assertIn('.config', path)


if __name__ == '__main__':
    unittest.main()