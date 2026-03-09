"""Tests for sections module."""

import unittest
from unittest.mock import patch
from generator.sections import (
    get_available_sections, get_section_info,
    validate_section, collect_section_data,
    SECTIONS
)


class TestSections(unittest.TestCase):
    """Test cases for section functions."""

    def test_get_available_sections_en(self):
        """Test getting available sections in English."""
        sections = get_available_sections('en')
        self.assertIn('installation', sections)
        self.assertIn('usage', sections)
        self.assertIn('license', sections)
        self.assertEqual(sections['installation'], 'Installation instructions')

    def test_get_available_sections_ru(self):
        """Test getting available sections in Russian."""
        sections = get_available_sections('ru')
        self.assertIn('installation', sections)
        self.assertEqual(sections['installation'], 'Инструкция по установке')

    def test_get_available_sections_fallback(self):
        """Test fallback to English for unknown language."""
        sections = get_available_sections('fr')
        self.assertEqual(sections['installation'], 'Installation instructions')

    def test_get_section_info(self):
        """Test getting section info."""
        info = get_section_info('installation', 'en')
        self.assertIsNotNone(info)
        self.assertEqual(info['prompt'], 'Installation instructions')
        self.assertTrue(info['multiline'])

        info = get_section_info('nonexistent', 'en')
        self.assertIsNone(info)

    def test_validate_section(self):
        """Test section validation."""
        self.assertTrue(validate_section('installation', 'en'))
        self.assertTrue(validate_section('usage', 'ru'))
        self.assertFalse(validate_section('nonexistent', 'en'))

    @patch('generator.sections.prompt_multiline')
    def test_collect_section_data_multiline(self, mock_prompt):
        """Test collecting data for multiline section."""
        mock_prompt.return_value = 'pip install .\npip install -e .'

        result = collect_section_data('installation', 'en')

        self.assertEqual(result, 'pip install .\npip install -e .')
        mock_prompt.assert_called_once_with("Enter Installation instructions", lang='en')

    @patch('generator.sections.prompt_input')
    def test_collect_section_data_singleline(self, mock_prompt):
        """Test collecting data for single line section."""
        mock_prompt.return_value = 'MIT'

        result = collect_section_data('license', 'en')

        self.assertEqual(result, 'MIT')
        mock_prompt.assert_called_once_with("Enter License", default='MIT', lang='en')

    def test_collect_section_data_nonexistent(self):
        """Test collecting data for nonexistent section."""
        result = collect_section_data('nonexistent', 'en')
        self.assertEqual(result, '')

    def test_section_structure(self):
        """Test that all sections have required fields."""
        for lang, sections in SECTIONS.items():
            for name, info in sections.items():
                self.assertIn('prompt', info)
                self.assertIn('multiline', info)
                self.assertIn('required', info)
                self.assertIn('description', info)

                if 'default' in info:
                    self.assertIsInstance(info['default'], str)


if __name__ == '__main__':
    unittest.main()