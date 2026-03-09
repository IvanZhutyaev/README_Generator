# README Generator

Усовершенствованный генератор README для проектов на GitHub с модульной структурой, поддержкой конфигураций, шаблонов, бейджей и локализацией.

## Возможности

- 📝 **Гибкая настройка секций**: описание, установка, использование, API, лицензия, авторы и другие
- 🎨 **Поддержка нескольких шаблонов**: Python, Web, универсальный и возможность создания своих
- 🏷️ **Генерация бейджей**: лицензия, версия Python с использованием shields.io
- ⚙️ **Сохранение конфигурации**: JSON-файлы для повторного использования настроек
- 💬 **Интерактивный режим**: пошаговый сбор данных с подсказками
- 🌍 **Локализация**: поддержка русского и английского языков
- 🧪 **Тестирование**: покрытие ключевых модулей тестами pytest

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

## Структура проекта

```
readme-generator-pro/
├── README.md                 # Документация
├── requirements.txt          # Зависимости (pytest)
├── .gitignore                # Игнорируемые файлы
├── setup.py                  # Установочный скрипт
├── generator/                # Основной модуль
│   ├── __init__.py           # Маркер пакета
│   ├── cli.py                # Интерфейс командной строки
│   ├── config.py             # Управление конфигурацией
│   ├── templates.py          # Загрузка шаблонов
│   ├── badges.py             # Генерация бейджей
│   ├── sections.py           # Определение секций
│   └── utils.py              # Вспомогательные функции
├── templates/                 # Папка с шаблонами
│   ├── default.md            # Универсальный шаблон (англ.)
│   ├── default_ru.md         # Универсальный шаблон (рус.)
│   └── python.md             # Шаблон для Python проектов
├── tests/                    # Тесты
│   ├── __init__.py
│   ├── test_cli.py           # Тесты CLI
│   └── test_config.py        # Тесты конфигурации
└── examples/                  # Примеры
    └── example_config.json    # Пример конфигурации
```

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
    "title": "My Awesome Project",
    "description": "This project does amazing things",
    "lang": "en",
    "template": "python",
    "output": "README.md",
    "sections": ["installation", "usage", "api", "license", "authors"],
    "section_data": {
        "installation": "pip install myproject",
        "usage": "import myproject\nmyproject.run()",
        "api": "TODO: Add API documentation",
        "license": "MIT",
        "authors": "John Doe <john@example.com>"
    },
    "python_version": "3.8"
}
```

## Запуск тестов

```bash
# Установка pytest
pip install pytest

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

MIT License. Подробнее см. в файле [LICENSE](LICENSE).

## Авторы

- Иван Жутяев (Ivan Zhutyaev)
  - Email: gitivanzhutyaev@gmail.com
  - GitHub: https://github.com/IvanZhutyaev

## Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в форк (`git push origin feature/amazing`)
5. Откройте Pull Request

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
