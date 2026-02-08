import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from catalog.models import Category, Product

print("=" * 70)
print("ПРОВЕРКА ВЫПОЛНЕНИЯ ДОМАШНЕЙ РАБОТЫ 2")
print("=" * 70)

# 1. Проверка PostgreSQL
print("\n1. БАЗА ДАННЫХ POSTGRESQL:")
print("-" * 40)
print(f"ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"NAME: {settings.DATABASES['default']['NAME']}")

# 2. Проверка моделей
print("\n2. МОДЕЛИ:")
print("-" * 40)
print(f"✓ Модель Category: {Category.__name__}")
print(f"  Поля: {[f.name for f in Category._meta.get_fields() if not f.is_relation]}")
print(f"✓ Модель Product: {Product.__name__}")
print(f"  Поля: {[f.name for f in Product._meta.get_fields() if not f.is_relation]}")

# 3. Проверка медиа
print("\n3. МЕДИАДАННЫЕ:")
print("-" * 40)
print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'НЕТ')}")
print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'НЕТ')}")

# 4. Проверка Pillow
try:
    from PIL import Image
    print(f"✓ Pillow установлен: {Image.__version__}")
except ImportError:
    print("✗ Pillow не установлен")

# 5. Проверка данных
print("\n4. ДАННЫЕ В БАЗЕ:")
print("-" * 40)
print(f"Категорий: {Category.objects.count()}")
print(f"Продуктов: {Product.objects.count()}")

# 6. Проверка фикстур
print("\n5. ФИКСТУРЫ:")
print("-" * 40)
fixtures_dir = os.path.join('catalog', 'fixtures')
if os.path.exists(fixtures_dir):
    files = os.listdir(fixtures_dir)
    print(f"✓ Папка существует, файлы: {files}")
else:
    print("✗ Папка не существует")

# 7. Проверка кастомной команды
print("\n6. КАСТОМНАЯ КОМАНДА:")
print("-" * 40)
cmd_path = os.path.join('catalog', 'management', 'commands', 'load_test_data.py')
if os.path.exists(cmd_path):
    print("✓ Команда load_test_data существует")
else:
    print("✗ Команда load_test_data не существует")

# 8. Проверка скриншотов
print("\n7. СКРИНШОТЫ:")
print("-" * 40)
if os.path.exists('screenshots'):
    screenshots = os.listdir('screenshots')
    print(f"✓ Папка screenshots существует")
    print(f"  Файлы: {screenshots}")
else:
    print("✗ Папка screenshots не существует")

print("\n" + "=" * 70)
print("РЕЗУЛЬТАТ ПРОВЕРКИ")
print("=" * 70)

# Подсчет выполненных пунктов
total = 0
passed = 0

checks = [
    ("PostgreSQL подключен", settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'),
    ("Модель Category создана", Category.__name__ == 'Category'),
    ("Модель Product создана", Product.__name__ == 'Product'),
    ("Поле image в Product", hasattr(Product, 'image')),
    ("MEDIA_URL настроен", hasattr(settings, 'MEDIA_URL') and settings.MEDIA_URL),
    ("MEDIA_ROOT настроен", hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT),
    ("Pillow установлен", 'Image' in locals()),
    ("Фикстуры созданы", os.path.exists(fixtures_dir) and len(os.listdir(fixtures_dir)) > 0),
    ("Кастомная команда создана", os.path.exists(cmd_path)),
]

for check_name, check_result in checks:
    total += 1
    if check_result:
        passed += 1
        print(f"✅ {check_name}")
    else:
        print(f"❌ {check_name}")

print(f"\n✅ Выполнено: {passed}/{total}")
print("=" * 70)
