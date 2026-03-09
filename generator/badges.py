"""Badge generation using shields.io."""

from typing import Dict, Any, List
import urllib.parse


class BadgeGenerator:
    """Generate badges for README."""

    def __init__(self):
        self.base_url = "https://img.shields.io/badge"

    def generate_license_badge(self, license_name: str) -> str:
        """Generate license badge."""
        if not license_name or license_name.lower() == 'none':
            return ""

        # Encode license name for URL
        encoded = urllib.parse.quote(license_name.replace(' ', '_'))
        color = self._get_license_color(license_name)

        badge = f"{self.base_url}/license-{encoded}-{color}.svg"
        return f"[![License]({badge})](LICENSE)"

    def generate_python_badge(self, version: str) -> str:
        """Generate Python version badge."""
        if not version:
            return ""

        encoded = urllib.parse.quote(version)
        badge = f"{self.base_url}/python-{encoded}-blue.svg"
        return f"![Python Version]({badge})"

    def generate_pypi_badge(self, package: str, version: str = None) -> str:
        """Generate PyPI badge."""
        if not package:
            return ""

        if version:
            badge = f"https://img.shields.io/pypi/v/{package}.svg"
        else:
            badge = f"https://img.shields.io/pypi/v/{package}.svg"

        return f"[![PyPI]({badge})](https://pypi.org/project/{package}/)"

    def generate_downloads_badge(self, package: str) -> str:
        """Generate PyPI downloads badge."""
        if not package:
            return ""

        badge = f"https://img.shields.io/pypi/dm/{package}.svg"
        return f"![Downloads]({badge})"

    def generate_build_badge(self, repo: str, branch: str = "main") -> str:
        """Generate GitHub Actions build badge."""
        if not repo:
            return ""

        encoded_repo = urllib.parse.quote(repo)
        badge = f"https://img.shields.io/github/actions/workflow/status/{encoded_repo}/ci.yml?branch={branch}"
        return f"[![Build Status]({badge})](https://github.com/{repo}/actions)"

    def generate_coverage_badge(self, coverage: str) -> str:
        """Generate code coverage badge."""
        if not coverage:
            return ""

        try:
            cov_num = int(coverage.replace('%', ''))
            color = self._get_coverage_color(cov_num)
        except ValueError:
            color = "yellow"

        badge = f"{self.base_url}/coverage-{coverage}-{color}.svg"
        return f"![Coverage]({badge})"

    def _get_license_color(self, license_name: str) -> str:
        """Get appropriate color for license badge."""
        license_colors = {
            'mit': 'green',
            'apache': 'blue',
            'gpl': 'orange',
            'bsd': 'yellow',
            'lgpl': 'lightgrey',
        }

        license_lower = license_name.lower()
        for key, color in license_colors.items():
            if key in license_lower:
                return color

        return "blue"

    def _get_coverage_color(self, coverage: int) -> str:
        """Get color based on coverage percentage."""
        if coverage >= 90:
            return "brightgreen"
        elif coverage >= 75:
            return "green"
        elif coverage >= 60:
            return "yellowgreen"
        elif coverage >= 40:
            return "yellow"
        elif coverage >= 20:
            return "orange"
        else:
            return "red"


def generate_badges(license_name: str, config: Dict[str, Any]) -> str:
    """
    Generate all configured badges.

    Args:
        license_name: License name for license badge
        config: Configuration dictionary

    Returns:
        String with all badges in Markdown format
    """
    generator = BadgeGenerator()
    badges = []

    # License badge
    if license_name:
        badge = generator.generate_license_badge(license_name)
        if badge:
            badges.append(badge)

    # Python version badge
    if config.get('python_version'):
        badge = generator.generate_python_badge(config['python_version'])
        if badge:
            badges.append(badge)

    # PyPI badge
    if config.get('pypi_package'):
        badge = generator.generate_pypi_badge(
            config['pypi_package'],
            config.get('pypi_version')
        )
        if badge:
            badges.append(badge)

    # Downloads badge
    if config.get('pypi_package') and config.get('show_downloads'):
        badge = generator.generate_downloads_badge(config['pypi_package'])
        if badge:
            badges.append(badge)

    # Build badge
    if config.get('github_repo'):
        badge = generator.generate_build_badge(
            config['github_repo'],
            config.get('branch', 'main')
        )
        if badge:
            badges.append(badge)

    # Coverage badge
    if config.get('coverage'):
        badge = generator.generate_coverage_badge(config['coverage'])
        if badge:
            badges.append(badge)

    # Join badges with spaces and add newlines
    if badges:
        return '\n'.join(badges) + '\n\n'

    return ""