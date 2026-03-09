"""Template management for README Generator Pro."""

import os
from typing import List, Optional
from .utils import get_package_dir, find_file

# Default template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(get_package_dir()), 'templates')


class TemplateNotFoundError(Exception):
    """Raised when template file is not found."""
    pass


class TemplateError(Exception):
    """Base exception for template errors."""
    pass


def list_templates() -> List[str]:
    """
    Return list of available template names (without extension).

    Returns:
        List of template names
    """
    if not os.path.exists(TEMPLATE_DIR):
        return []

    templates = set()
    try:
        for f in os.listdir(TEMPLATE_DIR):
            if f.endswith('.md') and not f.startswith('_'):
                name = f[:-3]  # remove .md
                # Handle language variants: name_lang.md
                parts = name.rsplit('_', 1)
                if len(parts) == 2 and parts[1] in ['en', 'ru']:
                    templates.add(parts[0])
                else:
                    templates.add(name)
    except OSError:
        return []

    return sorted(templates)


def get_template(template_name: str, lang: str = 'en') -> str:
    """
    Load template content for given name and language.

    Args:
        template_name: Name of the template
        lang: Language code ('en' or 'ru')

    Returns:
        Template content as string

    Raises:
        TemplateNotFoundError: If template not found
    """
    # Try language-specific template first
    lang_path = os.path.join(TEMPLATE_DIR, f"{template_name}_{lang}.md")
    if os.path.exists(lang_path):
        try:
            with open(lang_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            raise TemplateError(f"Unable to read template {lang_path}: {e}")

    # Try base template
    base_path = os.path.join(TEMPLATE_DIR, f"{template_name}.md")
    if os.path.exists(base_path):
        try:
            with open(base_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            raise TemplateError(f"Unable to read template {base_path}: {e}")

    # Try to find template in package
    package_path = find_file(f"templates/{template_name}_{lang}.md")
    if package_path and os.path.exists(package_path):
        try:
            with open(package_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            pass

    # If nothing found, raise error
    raise TemplateNotFoundError(
        f"Template '{template_name}' not found for language '{lang}'"
    )


def save_template(template_name: str, content: str, lang: str = 'en') -> str:
    """
    Save a new template to the templates directory.

    Args:
        template_name: Name of the template
        content: Template content
        lang: Language code

    Returns:
        Path to saved template
    """
    # Create templates directory if it doesn't exist
    if not os.path.exists(TEMPLATE_DIR):
        os.makedirs(TEMPLATE_DIR)

    # Determine filename
    if lang == 'en':
        filename = f"{template_name}.md"
    else:
        filename = f"{template_name}_{lang}.md"

    filepath = os.path.join(TEMPLATE_DIR, filename)

    # Save template
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def validate_template(content: str) -> bool:
    """
    Validate that template has all required placeholders.

    Args:
        content: Template content to validate

    Returns:
        True if valid, False otherwise
    """
    required = ['{title}', '{description}']
    optional = ['{badges}', '{installation}', '{usage}', '{api}',
                '{license}', '{authors}', '{contributing}']

    # Check required placeholders
    for req in required:
        if req not in content:
            return False

    return True


# Default template as fallback
DEFAULT_TEMPLATE = """# {title}

{badges}
{description}

## Installation

{installation}

## Usage

{usage}

## License

{license}
"""

# Russian default template
DEFAULT_TEMPLATE_RU = """# {title}

{badges}
{description}

## Установка

{installation}

## Использование

{usage}

## Лицензия

{license}
"""