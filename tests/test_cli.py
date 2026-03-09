"""Tests for CLI module."""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import tempfile
from generator.cli import ReadmeGeneratorCLI, main


class TestCLI(unittest.TestCase):
    """Test cases for CLI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = ReadmeGeneratorCLI()

    @patch('sys.argv', ['cli.py', '--list-templates'])
    @patch('generator.cli.print_info')
    @patch('generator.cli.list_templates')
    def test_list_templates(self, mock_list, mock_print):
        """Test --list-templates option."""
        mock_list.return_value = ['default', 'python']

        with self.assertRaises(SystemExit) as cm:
            self.cli.run()

        self.assertEqual(cm.exception.code, 0)
        mock_print.assert_called_with("Available templates:")
        mock_list.assert_called_once()

    @patch('sys.argv', ['cli.py', '--title', 'Test Project', '--no-interactive'])
    @patch('generator.cli.print_error')
    def test_missing_data_non_interactive(self, mock_error):
        """Test non-interactive mode with missing data."""
        with self.assertRaises(SystemExit) as cm:
            self.cli.run()

        self.assertEqual(cm.exception.code, 1)
        mock_error.assert_called_once()

    @patch('sys.argv', ['cli.py', '--config', 'nonexistent.json', '--no-interactive'])
    @patch('generator.cli.print_error')
    def test_config_not_found(self, mock_error):
        """Test handling of missing config file."""
        with self.assertRaises(SystemExit) as cm:
            self.cli.run()

        self.assertEqual(cm.exception.code, 1)

    @patch('sys.argv', ['cli.py'])
    @patch('generator.cli.prompt_input')
    @patch('generator.cli.prompt_multiline')
    @patch('generator.cli.write_file')
    @patch('generator.cli.list_templates')
    def test_interactive_mode(self, mock_list, mock_write, mock_multiline, mock_input):
        """Test interactive mode with all inputs."""
        mock_list.return_value = ['default', 'python']

        # Mock user inputs
        mock_input.side_effect = [
            'My Project',  # title
            'A test project',  # description
            'installation,usage',  # sections
            'default'  # template
        ]

        mock_multiline.side_effect = [
            'pip install .\npip install -e .',  # installation
            'python example.py'  # usage
        ]

        self.cli.run()

        # Verify write_file was called
        mock_write.assert_called_once()
        args, kwargs = mock_write.call_args
        self.assertEqual(args[0], 'README.md')
        content = args[1]
        self.assertIn('# My Project', content)
        self.assertIn('A test project', content)


class TestMainFunction(unittest.TestCase):
    """Test the main entry point."""

    @patch('generator.cli.ReadmeGeneratorCLI')
    def test_main(self, mock_cli_class):
        """Test main function creates CLI and runs it."""
        mock_instance = MagicMock()
        mock_cli_class.return_value = mock_instance

        main()

        mock_cli_class.assert_called_once()
        mock_instance.run.assert_called_once()


if __name__ == '__main__':
    unittest.main()