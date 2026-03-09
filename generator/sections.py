"""Section management for README Generator Pro."""

from typing import Dict, Any, Optional
from .utils import prompt_input, prompt_multiline

# Section definitions with prompts in different languages
SECTIONS = {
    'en': {
        'installation': {
            'prompt': 'Installation instructions',
            'multiline': True,
            'required': False,
            'description': 'How to install your project'
        },
        'usage': {
            'prompt': 'Usage examples',
            'multiline': True,
            'required': False,
            'description': 'Examples of how to use your project'
        },
        'api': {
            'prompt': 'API documentation',
            'multiline': True,
            'required': False,
            'description': 'Description of API endpoints or functions'
        },
        'contributing': {
            'prompt': 'Contributing guidelines',
            'multiline': True,
            'required': False,
            'description': 'How others can contribute to your project'
        },
        'license': {
            'prompt': 'License',
            'multiline': False,
            'required': False,
            'description': 'Project license (e.g., MIT, Apache-2.0)',
            'default': 'MIT'
        },
        'authors': {
            'prompt': 'Authors',
            'multiline': True,
            'required': False,
            'description': 'List of project authors and contributors'
        },
        'changelog': {
            'prompt': 'Changelog',
            'multiline': True,
            'required': False,
            'description': 'Version history and changes'
        },
        'requirements': {
            'prompt': 'Requirements',
            'multiline': True,
            'required': False,
            'description': 'Project dependencies and system requirements'
        },
        'configuration': {
            'prompt': 'Configuration',
            'multiline': True,
            'required': False,
            'description': 'Configuration options and environment variables'
        },
        'testing': {
            'prompt': 'Testing',
            'multiline': True,
            'required': False,
            'description': 'How to run tests'
        },
        'examples': {
            'prompt': 'Examples',
            'multiline': True,
            'required': False,
            'description': 'Additional examples'
        },
        'faq': {
            'prompt': 'FAQ',
            'multiline': True,
            'required': False,
            'description': 'Frequently asked questions'
        },
        'support': {
            'prompt': 'Support',
            'multiline': True,
            'required': False,
            'description': 'Where to get help'
        },
        'acknowledgments': {
            'prompt': 'Acknowledgments',
            'multiline': True,
            'required': False,
            'description': 'Credits and acknowledgments'
        }
    },
    'ru': {
        'installation': {
            'prompt': 'Инструкция по установке',
            'multiline': True,
            'required': False,
            'description': 'Как установить проект'
        },
        'usage': {
            'prompt': 'Примеры использования',
            'multiline': True,
            'required': False,
            'description': 'Примеры использования проекта'
        },
        'api': {
            'prompt': 'Документация API',
            'multiline': True,
            'required': False,
            'description': 'Описание API функций или эндпоинтов'
        },
        'contributing': {
            'prompt': 'Правила внесения вклада',
            'multiline': True,
            'required': False,
            'description': 'Как другие могут внести вклад в проект'
        },
        'license': {
            'prompt': 'Лицензия',
            'multiline': False,
            'required': False,
            'description': 'Лицензия проекта (например, MIT)',
            'default': 'MIT'
        },
        'authors': {
            'prompt': 'Авторы',
            'multiline': True,
            'required': False,
            'description': 'Список авторов и контрибьюторов'
        },
        'changelog': {
            'prompt': 'История изменений',
            'multiline': True,
            'required': False,
            'description': 'История версий и изменений'
        },
        'requirements': {
            'prompt': 'Требования',
            'multiline': True,
            'required': False,
            'description': 'Зависимости и системные требования'
        },
        'configuration': {
            'prompt': 'Конфигурация',
            'multiline': True,
            'required': False,
            'description': 'Параметры конфигурации и переменные окружения'
        },
        'testing': {
            'prompt': 'Тестирование',
            'multiline': True,
            'required': False,
            'description': 'Как запускать тесты'
        },
        'examples': {
            'prompt': 'Примеры',
            'multiline': True,
            'required': False,
            'description': 'Дополнительные примеры'
        },
        'faq': {
            'prompt': 'Часто задаваемые вопросы',
            'multiline': True,
            'required': False,
            'description': 'Часто задаваемые вопросы'
        },
        'support': {
            'prompt': 'Поддержка',
            'multiline': True,
            'required': False,
            'description': 'Где получить помощь'
        },
        'acknowledgments': {
            'prompt': 'Благодарности',
            'multiline': True,
            'required': False,
            'description': 'Благодарности и признания'
        }
    }
}


def get_available_sections(lang: str = 'en') -> Dict[str, str]:
    """
    Return dict of section names and their prompts for given language.

    Args:
        lang: Language code ('en' or 'ru')

    Returns:
        Dictionary mapping section names to prompts
    """
    if lang not in SECTIONS:
        lang = 'en'

    return {name: info['prompt'] for name, info in SECTIONS[lang].items()}


def get_section_info(section_name: str, lang: str = 'en') -> Optional[Dict[str, Any]]:
    """
    Get section information.

    Args:
        section_name: Name of the section
        lang: Language code

    Returns:
        Section info dictionary or None if not found
    """
    if lang not in SECTIONS:
        lang = 'en'

    return SECTIONS[lang].get(section_name)


def validate_section(section_name: str, lang: str = 'en') -> bool:
    """
    Validate that section exists.

    Args:
        section_name: Name of the section
        lang: Language code

    Returns:
        True if section exists, False otherwise
    """
    return section_name in SECTIONS.get(lang, {})


def collect_section_data(section_name: str, lang: str = 'en') -> str:
    """
    Prompt user for data for a specific section.

    Args:
        section_name: Name of the section
        lang: Language code

    Returns:
        String with section content
    """
    info = get_section_info(section_name, lang)
    if not info:
        return ''

    prompt_text = info['prompt']

    if info.get('multiline', False):
        return prompt_multiline(f"Enter {prompt_text}", lang=lang)
    else:
        default = info.get('default', '')
        return prompt_input(
            f"Enter {prompt_text}",
            default=default,
            lang=lang
        )