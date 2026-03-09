"""Tests for badges module."""

import unittest
from generator.badges import BadgeGenerator, generate_badges


class TestBadges(unittest.TestCase):
    """Test cases for badge functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = BadgeGenerator()

    def test_license_badge(self):
        """Test license badge generation."""
        badge = self.generator.generate_license_badge('MIT')
        self.assertIn('license-MIT', badge)
        self.assertIn('green', badge)

        badge = self.generator.generate_license_badge('Apache 2.0')
        self.assertIn('license-Apache_2.0', badge)

    def test_license_badge_empty(self):
        """Test license badge with empty license."""
        badge = self.generator.generate_license_badge('')
        self.assertEqual(badge, '')

        badge = self.generator.generate_license_badge('none')
        self.assertEqual(badge, '')

    def test_python_badge(self):
        """Test Python version badge."""
        badge = self.generator.generate_python_badge('3.8')
        self.assertIn('python-3.8', badge)
        self.assertIn('blue', badge)

        badge = self.generator.generate_python_badge('')
        self.assertEqual(badge, '')

    def test_pypi_badge(self):
        """Test PyPI badge."""
        badge = self.generator.generate_pypi_badge('requests')
        self.assertIn('pypi/v/requests', badge)
        self.assertIn('pypi.org', badge)

        badge = self.generator.generate_pypi_badge('')
        self.assertEqual(badge, '')

    def test_downloads_badge(self):
        """Test downloads badge."""
        badge = self.generator.generate_downloads_badge('requests')
        self.assertIn('pypi/dm/requests', badge)

        badge = self.generator.generate_downloads_badge('')
        self.assertEqual(badge, '')

    def test_build_badge(self):
        """Test build badge."""
        badge = self.generator.generate_build_badge('user/repo')
        self.assertIn('user/repo', badge)
        self.assertIn('actions/workflow', badge)

        badge = self.generator.generate_build_badge('')
        self.assertEqual(badge, '')

    def test_coverage_badge(self):
        """Test coverage badge."""
        badge = self.generator.generate_coverage_badge('85%')
        self.assertIn('coverage-85%25', badge)
        self.assertIn('yellowgreen', badge)

        badge = self.generator.generate_coverage_badge('')
        self.assertEqual(badge, '')

    def test_coverage_color(self):
        """Test coverage color logic."""
        self.assertEqual(self.generator._get_coverage_color(95), 'brightgreen')
        self.assertEqual(self.generator._get_coverage_color(80), 'green')
        self.assertEqual(self.generator._get_coverage_color(70), 'yellowgreen')
        self.assertEqual(self.generator._get_coverage_color(50), 'yellow')
        self.assertEqual(self.generator._get_coverage_color(30), 'orange')
        self.assertEqual(self.generator._get_coverage_color(10), 'red')

    def test_license_color(self):
        """Test license color logic."""
        self.assertEqual(self.generator._get_license_color('MIT'), 'green')
        self.assertEqual(self.generator._get_license_color('Apache'), 'blue')
        self.assertEqual(self.generator._get_license_color('GPL'), 'orange')
        self.assertEqual(self.generator._get_license_color('unknown'), 'blue')

    def test_generate_badges_function(self):
        """Test the main generate_badges function."""
        config = {
            'python_version': '3.8',
            'pypi_package': 'test-package',
            'github_repo': 'user/repo',
            'coverage': '85%'
        }

        result = generate_badges('MIT', config)
        self.assertIn('license-MIT', result)
        self.assertIn('python-3.8', result)
        self.assertIn('pypi/v/test-package', result)
        self.assertIn('user/repo', result)
        self.assertIn('coverage-85%25', result)


if __name__ == '__main__':
    unittest.main()