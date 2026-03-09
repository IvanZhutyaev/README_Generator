#!/usr/bin/env python3
"""
Command-line interface for README Generator Pro.
Handles argument parsing, interactive input, and orchestrates the generation process.
"""

import argparse
import sys
import os
from typing import Dict, Any, List
from .config import load_config, save_config, merge_with_defaults
from .templates import get_template, list_templates, TemplateNotFoundError
from .sections import collect_section_data, get_available_sections, validate_section
from .badges import generate_badges
from .utils import (
    prompt_input,
    prompt_multiline,
    write_file,
    load_sections_from_string,
    validate_filename,
    print_error,
    print_success,
    print_info,
    print_warning
)


class ReadmeGeneratorCLI:
    """Main CLI class for README generation."""

    def __init__(self):
        self.args = None
        self.config = {}

    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="README Generator Pro - Advanced README generator for GitHub",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python -m generator.cli
  python -m generator.cli --title "My Project" --sections installation,usage
  python -m generator.cli --config project.json
  python -m generator.cli --list-templates
  python -m generator.cli --lang ru --template python
            """
        )

        parser.add_argument(
            '--config',
            help='Path to JSON configuration file'
        )

        parser.add_argument(
            '--title',
            help='Project title'
        )

        parser.add_argument(
            '--description',
            help='Project description'
        )

        parser.add_argument(
            '--sections',
            help='Comma-separated list of sections to include (e.g., installation,usage,license)'
        )

        parser.add_argument(
            '--template',
            help='Template name (default, python, web)'
        )

        parser.add_argument(
            '--lang',
            default='en',
            choices=['en', 'ru'],
            help='Language for section prompts and output (default: en)'
        )

        parser.add_argument(
            '--output',
            default='README.md',
            help='Output file name (default: README.md)'
        )

        parser.add_argument(
            '--save-config',
            help='Save provided options to a config file'
        )

        parser.add_argument(
            '--list-templates',
            action='store_true',
            help='List available templates and exit'
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.2.0'
        )

        parser.add_argument(
            '--no-interactive',
            action='store_true',
            help='Disable interactive mode (fail if required data missing)'
        )

        parser.add_argument(
            '--python-version',
            help='Python version for badge (e.g., 3.8, 3.9+)'
        )

        return parser.parse_args()

    def list_templates_and_exit(self) -> None:
        """List available templates and exit."""
        templates = list_templates()
        print_info("Available templates:")
        for tmpl in templates:
            print(f"  • {tmpl}")
        print_info("\nUse --template <name> to select a template")
        sys.exit(0)

    def load_initial_config(self) -> Dict[str, Any]:
        """Load configuration from file if specified."""
        config = {}
        if self.args and self.args.config:
            try:
                config = load_config(self.args.config)
                print_success(f"Loaded configuration from {self.args.config}")
            except FileNotFoundError:
                print_error(f"Config file not found: {self.args.config}")
                if self.args.no_interactive:
                    sys.exit(1)
                print_warning("Continuing with default configuration...")
            except ValueError as e:
                print_error(f"Invalid config file: {e}")
                if self.args.no_interactive:
                    sys.exit(1)
                print_warning("Continuing with default configuration...")
        return config

    def merge_cli_args(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge command line arguments into config."""
        if self.args.title:
            config['title'] = self.args.title
        if self.args.description:
            config['description'] = self.args.description
        if self.args.template:
            config['template'] = self.args.template
        if self.args.lang:
            config['lang'] = self.args.lang
        if self.args.output:
            config['output'] = self.args.output
        if self.args.sections:
            config['sections'] = [s.strip() for s in self.args.sections.split(',')]
        if self.args.python_version:
            config['python_version'] = self.args.python_version

        return config

    def collect_interactive_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Collect missing data interactively."""
        if self.args.no_interactive:
            # Check if all required data is present
            required = ['title', 'description', 'sections', 'template']
            missing = [r for r in required if r not in config or not config[r]]
            if missing:
                print_error(f"Missing required data in non-interactive mode: {', '.join(missing)}")
                sys.exit(1)
            return config

        lang = config.get('lang', 'en')

        # Collect title if missing
        if 'title' not in config or not config['title']:
            config['title'] = prompt_input(
                "Enter project title",
                lang=lang
            )

        # Collect description if missing
        if 'description' not in config or not config['description']:
            config['description'] = prompt_input(
                "Enter project description",
                lang=lang
            )

        # Collect sections if missing
        if 'sections' not in config or not config['sections']:
            available = get_available_sections(lang)
            print_info("Available sections: " + ", ".join(available.keys()))
            sections_str = prompt_input(
                "Enter sections to include (comma-separated)",
                default="installation,usage,license",
                lang=lang
            )
            config['sections'] = load_sections_from_string(sections_str, available.keys())

        # Collect template if missing
        if 'template' not in config or not config['template']:
            templates = list_templates()
            if not templates:
                print_warning("No templates found, using default")
                config['template'] = 'default'
            else:
                default_template = 'default' if 'default' in templates else templates[0]
                config['template'] = prompt_input(
                    f"Choose template ({', '.join(templates)})",
                    default=default_template,
                    lang=lang
                )

        return config

    def collect_section_data_interactive(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data for each selected section."""
        lang = config.get('lang', 'en')
        sections = config.get('sections', [])
        existing_data = config.get('section_data', {})

        for section in sections:
            if section not in existing_data or not existing_data[section]:
                print_info(f"\n--- Section: {section} ---")
                if validate_section(section, lang):
                    existing_data[section] = collect_section_data(section, lang=lang)

        config['section_data'] = existing_data
        return config

    def generate_readme(self, config: Dict[str, Any]) -> str:
        """Generate README content from template and data."""
        # Generate badges
        badges = generate_badges(
            config.get('section_data', {}).get('license', ''),
            config
        )

        # Load template
        try:
            template_content = get_template(
                config['template'],
                lang=config.get('lang', 'en')
            )
        except TemplateNotFoundError as e:
            print_error(f"Template error: {e}")
            print_warning("Using default template...")
            from .templates import DEFAULT_TEMPLATE
            template_content = DEFAULT_TEMPLATE

        # Prepare context
        context = {
            'title': config['title'],
            'description': config['description'],
            'badges': badges,
            **config.get('section_data', {})
        }

        # Fill template
        try:
            return template_content.format(**context)
        except KeyError as e:
            print_error(f"Missing key in template: {e}")
            print_warning("Available context keys: " + ", ".join(context.keys()))
            sys.exit(1)

    def run(self) -> None:
        """Main execution method."""
        # Parse arguments
        self.args = self.parse_arguments()

        # Handle --list-templates
        if self.args.list_templates:
            self.list_templates_and_exit()

        # Load configuration
        self.config = self.load_initial_config()

        # Merge CLI arguments
        self.config = self.merge_cli_args(self.config)

        # Apply defaults
        self.config = merge_with_defaults(self.config)

        # Validate output filename
        if not validate_filename(self.config.get('output', 'README.md')):
            print_error("Invalid output filename")
            sys.exit(1)

        try:
            # Collect missing data interactively
            self.config = self.collect_interactive_data(self.config)

            # Collect section data
            self.config = self.collect_section_data_interactive(self.config)

            # Generate README
            readme_content = self.generate_readme(self.config)

            # Write to file
            write_file(self.config['output'], readme_content)
            print_success(f"README successfully generated: {self.config['output']}")

            # Save config if requested
            if self.args.save_config:
                save_config(self.args.save_config, self.config)
                print_success(f"Configuration saved to {self.args.save_config}")

        except KeyboardInterrupt:
            print_error("\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            if not self.args.no_interactive:
                import traceback
                traceback.print_exc()
            sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli = ReadmeGeneratorCLI()
    cli.run()


if __name__ == "__main__":
    main()