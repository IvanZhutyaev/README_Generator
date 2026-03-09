"""Utility functions for README Generator Pro."""

import os
import sys
from typing import List, Optional
from pathlib import Path


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_color(message: str, color: str) -> None:
    """Print colored message to terminal."""
    if sys.stdout.isatty():  # Check if terminal supports colors
        print(f"{color}{message}{Colors.END}")
    else:
        print(message)


def print_success(message: str) -> None:
    """Print success message in green."""
    print_color(f"✓ {message}", Colors.GREEN)


def print_error(message: str) -> None:
    """Print error message in red."""
    print_color(f"✗ {message}", Colors.RED)


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print_color(f"⚠ {message}", Colors.YELLOW)


def print_info(message: str) -> None:
    """Print info message in blue."""
    print_color(f"ℹ {message}", Colors.BLUE)


def get_package_dir() -> str:
    """
    Return the directory of the current package.

    Returns:
        Absolute path to package directory
    """
    return os.path.dirname(os.path.abspath(__file__))


def find_file(filename: str) -> Optional[str]:
    """
    Find file in package directory or subdirectories.

    Args:
        filename: Name of file to find

    Returns:
        Full path to file if found, None otherwise
    """
    package_dir = get_package_dir()

    # Walk through package directory
    for root, dirs, files in os.walk(package_dir):
        if filename in files:
            return os.path.join(root, filename)

    return None


def prompt_input(message: str, default: Optional[str] = None, lang: str = 'en') -> str:
    """
    Prompt user for input with optional default value.

    Args:
        message: Prompt message
        default: Default value if user enters nothing
        lang: Language code (for future use)

    Returns:
        User input string
    """
    if default:
        full_message = f"{message} [{default}]: "
    else:
        full_message = f"{message}: "

    try:
        value = input(full_message).strip()
        if not value and default is not None:
            return default
        return value
    except (KeyboardInterrupt, EOFError):
        print("\n")
        raise


def prompt_multiline(message: str, lang: str = 'en') -> str:
    """
    Prompt for multi-line input, terminated by empty line.

    Args:
        message: Prompt message
        lang: Language code (for future use)

    Returns:
        Multi-line string
    """
    print(message + " (enter an empty line to finish):")
    lines = []
    try:
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
    except (KeyboardInterrupt, EOFError):
        print("\n")
        raise

    return "\n".join(lines)


def load_sections_from_string(sections_str: str, allowed_sections: List[str]) -> List[str]:
    """
    Parse comma-separated section list, filtering allowed sections.

    Args:
        sections_str: Comma-separated string of section names
        allowed_sections: List of allowed section names

    Returns:
        List of valid section names
    """
    if not sections_str:
        return []

    parts = [s.strip() for s in sections_str.split(',')]
    return [p for p in parts if p in allowed_sections]


def validate_filename(filename: str) -> bool:
    """
    Validate that filename is safe to write.

    Args:
        filename: Filename to validate

    Returns:
        True if valid, False otherwise
    """
    # Check for path traversal
    if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
        return False

    # Check for invalid characters
    invalid_chars = '<>:"|?*'
    if any(c in filename for c in invalid_chars):
        return False

    return True


def write_file(path: str, content: str) -> None:
    """
    Write content to file, creating directories if needed.

    Args:
        path: File path
        content: Content to write

    Raises:
        IOError: If unable to write file
    """
    # Create directory if it doesn't exist
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    # Write file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_file(path: str) -> str:
    """
    Read content from file.

    Args:
        path: File path

    Returns:
        File content

    Raises:
        FileNotFoundError: If file not found
        IOError: If unable to read file
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def ensure_directory(path: str) -> None:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        path: Directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)