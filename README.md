## Описание проекта
Skystore - это платформа для продажи цифровых товаров: плагинов, утилит, микросервисов и примеров кода.

## Технологии
- Python 3.11+
- Django 4.2+
- Bootstrap 5
- SQLite (для разработки)

## Установка и запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Запустить миграции: `python manage.py migrate`
6. Запустить сервер: `python manage.py runserver`

## Структура проекта
- `catalog/` - основное приложение магазина
- `templates/` - HTML шаблоны
- `config/` - настройки Django

## Лицензия
MIT
EOF