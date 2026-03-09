## Анализатор логов

Инструмент для анализа логов Nginx, генерации статистики и отчётов. 

## Установка 

1. Клонирование репозитория
```git clone https://github.com/VeraAdzhieva/parser_logs.git```
2. Создание виртуального окружения и активация
```python3 -m venv venv```
```source venv/bin/activate```
3. Установка зависимостей
```poetry install```

## Основные зависимости
Ключевые библиотеки:
- **structlog** — структурированное логирование
- **pytest** — тестирование
- **black, isort, flake8, mypy** — форматирование и статический анализ кода

*Полный список зависимостей доступен в `pyproject.toml`.*

## Запуск тестов
```poetry run pytest -v```

## Запуск pre-commit
```poetry run pre-commit run --all-files```

## Пример запуска кода
- ```poetry run python log_analyzer.py```
- ```poetry run python log_analyzer.py --input path/logfile.log``` (с указанием пути к файлу логов)