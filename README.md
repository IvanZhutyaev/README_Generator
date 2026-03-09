# README Generator

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)

Инструмент командной строки для автоматической генерации качественного `README.md` для проектов на GitHub.  
Поддерживает интерактивный режим, конфигурационные файлы, шаблоны, генерацию бейджей и локализацию (RU/EN).

## Цели и возможности

- 📝 **Упрощение создания README**: быстрое заполнение типовых разделов (installation, usage, api, license, authors и др.).
- 🎛️ **Гибкая структура**: выбор нужных секций и шаблонов под конкретный проект (универсальный, Python, Web, собственные шаблоны).
- 🌍 **Многоязычность**: генерация README на русском и английском; локализованные шаблоны (`default.md`, `default_ru.md`).
- 🏷️ **Бейджи shields.io**: лицензия, версия Python, PyPI, загрузки, статус сборки GitHub Actions, покрытие кода.
- 💾 **Конфигурации в JSON**: сохранение и повторное использование настроек проекта.
- 💬 **Интерактивный режим**: пошаговый опрос с многострочным вводом там, где нужно.
- 🧪 **Тестируемость**: модульная архитектура (`generator/*`) и тесты в `tests/`.

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/IvanZhutyaev/README_Generator.git
cd README_Generator

# Установка зависимостей для разработки
pip install -r requirements.txt
```

## Быстрый старт

### Интерактивный режим

```bash
readme-gen

# или напрямую модуль
python -m generator.cli
```

Скрипт последовательно запросит все необходимые данные:
- Название проекта
- Описание
- Секции для включения
- Данные для каждой секции
- Выбор шаблона

### Режим командной строки

```bash
python -m generator.cli \
  --title "My Project" \
  --description "Awesome project description" \
  --sections installation,usage,license \
  --template python \
  --lang ru \
  --output README.md
```

### Использование конфигурационного файла

```bash
python -m generator.cli --config examples/example_config.json
```

### Сохранение конфигурации

```bash
python -m generator.cli --title "My Project" --save-config myproject.json
```

## Параметры командной строки

| Параметр | Описание |
|----------|----------|
| `--config PATH` | Загрузить конфигурацию из JSON файла |
| `--title TEXT` | Название проекта |
| `--description TEXT` | Описание проекта |
| `--sections LIST` | Список секций через запятую (installation,usage,license,api,authors) |
| `--template NAME` | Имя шаблона (default, python, web) |
| `--lang en\|ru` | Язык интерфейса (по умолчанию: en) |
| `--output FILE` | Имя выходного файла (по умолчанию: README.md) |
| `--save-config PATH` | Сохранить текущую конфигурацию в файл |
| `--list-templates` | Показать доступные шаблоны |
| `--no-interactive` | Отключить интерактивный режим (ошибка, если не хватает данных) |
| `--python-version` | Версия Python для бейджа (например, `3.8`, `3.9+`) |

## Архитектура и структура проекта

Проект организован как Python‑пакет с модульной архитектурой.

```text
README_Generator/
├── README.md                  # Документация проекта
├── requirements.txt           # Зависимости (pytest, pytest-cov)
├── setup.py                   # Установочный скрипт (entry point readme-gen)
├── pyproject.toml             # Современная конфигурация проекта
├── MANIFEST.in                # Включение шаблонов и лицензии в дистрибутив
├── LICENSE                    # Лицензия MIT
├── generator/                 # Основной пакет
│   ├── __init__.py            # Метаданные пакета и экспорт API
│   ├── cli.py                 # CLI, аргументы, интерактивный режим, генерация README
│   ├── config.py              # Загрузка/сохранение/валидация конфигурации
│   ├── templates.py           # Управление шаблонами README
│   ├── badges.py              # Генерация бейджей shields.io
│   ├── sections.py            # Описание секций и сбор данных
│   └── utils.py               # Ввод/вывод, цвета, работа с файлами
├── templates/                 # Шаблоны Markdown
│   ├── default.md             # Универсальный шаблон (EN)
│   ├── default_ru.md          # Универсальный шаблон (RU)
│   ├── python.md              # Шаблон для Python‑проектов
│   └── web.md                 # Шаблон для Web‑проектов
├── tests/                     # Модульные тесты (unittest/pytest)
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_templates.py
│   ├── test_badges.py
│   ├── test_sections.py
│   └── test_utils.py
└── examples/                  # Примеры конфигураций
    ├── example_config.json
    ├── simple_config.json
    └── russian_config.json
```

Кратко по основным модулям:

- `generator/cli.py`: парсинг аргументов, загрузка/слияние конфигураций, интерактивный режим, генерация и запись `README.md`.
- `generator/config.py`: `DEFAULT_CONFIG`, загрузка/сохранение JSON, валидация и слияние с дефолтами, путь к конфигам в `~/.config/readme-generator/`.
- `generator/templates.py`: поиск и загрузка шаблонов (`list_templates`, `get_template`, `save_template`, `validate_template`), fallback‑шаблоны.
- `generator/badges.py`: класс `BadgeGenerator` и функция `generate_badges` для лицензии, Python, PyPI, скачиваний, статуса билда и покрытия.
- `generator/sections.py`: многоязычный словарь `SECTIONS`, валидация и интерактивный сбор данных по секциям.
- `generator/utils.py`: цветной вывод, безопасная запись файлов, валидация имён, поиск файлов пакета, функции ввода.

## Создание собственных шаблонов

Шаблоны находятся в папке `templates/`. Вы можете создавать свои:

1. Создайте файл `templates/mytemplate.md`
2. Используйте плейсхолдеры в фигурных скобках: `{title}`, `{description}`, `{installation}`, `{usage}`, `{api}`, `{license}`, `{authors}`, `{badges}`
3. Для локализации создайте `mytemplate_ru.md`

### Пример шаблона:

```markdown
# {title}

{badges}
{description}

## 📦 Установка

{installation}

## 🚀 Использование

{usage}

## 📖 API

{api}

## 👥 Авторы

{authors}

## 📄 Лицензия

{license}
```

## Конфигурационные файлы

Пример `config.json`:

```json
{
  "title": "README Generator",
  "description": "CLI tool that generates professional README files from templates and JSON configuration",
  "lang": "en",
  "template": "python",
  "output": "README.md",
  "sections": ["installation", "usage", "api", "license", "authors"],
  "section_data": {
    "installation": "pip install -r requirements.txt",
    "usage": "python -m generator.cli --config .readme-config.json",
    "api": "See generator/cli.py and generator/templates.py for public API",
    "license": "MIT",
    "authors": "Ivan Zhutyaev <gitivanzhutyaev@gmail.com>"
  },
  "python_version": "3.8",
  "github_repo": "IvanZhutyaev/README_Generator"
}
```

### Примеры из директории `examples/`

- `examples/example_config.json` — полный пример с PyPI/CI/coverage‑бейджами.
- `examples/simple_config.json` — минимальная конфигурация.
- `examples/russian_config.json` — конфигурация на русском языке.

## Запуск тестов

```bash
# Установка зависимостей для тестирования
pip install -r requirements.txt

# Запуск всех тестов
pytest tests/

# Запуск с детализацией
pytest tests/ -v

# Проверка покрытия
pytest tests/ --cov=generator
```

## Расширение функциональности

### Добавление новой секции

1. Добавьте секцию в `generator/sections.py` в словарь `SECTIONS` для каждого языка:

```python
SECTIONS = {
    'en': {
        # ... существующие секции
        'changelog': 'Changelog',  # новая секция
    },
    'ru': {
        # ... существующие секции
        'changelog': 'История изменений',
    }
}
```

2. Добавьте соответствующий плейсхолдер `{changelog}` в шаблоны

### Добавление нового типа бейджа

В `generator/badges.py` добавьте логику генерации:

```python
def generate_badges(license_name, config):
    badges = []
    # ... существующие бейджи
    
    if 'coverage' in config:
        coverage = config['coverage']
        badge_url = f"https://img.shields.io/badge/coverage-{coverage}%25-brightgreen"
        badges.append(f"![Coverage]({badge_url})")
    
    return ' '.join(badges) + '\n\n' if badges else ''
```

## Лицензия

MIT License. Подробнее см. в файле `LICENSE`.

## Авторы

- Иван Жутяев (Ivan Zhutyaev)
  - Email: gitivanzhutyaev@gmail.com
  - GitHub: https://github.com/IvanZhutyaev

## Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий `README_Generator`.
2. Создайте ветку для новой функции (`git checkout -b feature/my-feature`).
3. Зафиксируйте изменения (`git commit -m "Add my feature"`).
4. Отправьте изменения в свой форк (`git push origin feature/my-feature`).
5. Откройте Pull Request в основной репозиторий.

## Часто задаваемые вопросы

### Как добавить свой шаблон?
Поместите файл `.md` в папку `templates/`. Для многоязычности создайте `имя_ru.md`.

### Можно ли генерировать README для приватных проектов?
Да, генератор работает локально и не требует доступа к интернету (кроме загрузки бейджей).

### Поддерживаются ли другие языки, кроме английского и русского?
Да, вы можете добавить поддержку любого языка, расширив словари в `sections.py` и создав локализованные шаблоны.

## Благодарности

- [shields.io](https://shields.io) за генерацию бейджей
- Сообществу Python за вдохновение
