"""
README Generator
~~~~~~~~~~~~~~~~

Advanced README generator for GitHub projects with template support,
badges, localization, and configuration management.

:copyright: (c) 2024 by Ivan Zhutyaev
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.2.0"
__author__ = "Ivan Zhutyaev"
__license__ = "MIT"

from .cli import main
from .config import load_config, save_config
from .templates import get_template, list_templates
from .sections import get_available_sections, collect_section_data

__all__ = [
    'main',
    'load_config',
    'save_config',
    'get_template',
    'list_templates',
    'get_available_sections',
    'collect_section_data',
]