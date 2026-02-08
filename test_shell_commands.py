print("=" * 60)
print("ВЫПОЛНЕНИЕ ЗАДАНИЙ ИЗ SHELL")
print("=" * 60)

# Импорт моделей
from catalog.models import Category, Product

print("\n1. Создание категорий:")
print("-" * 40)

# Удаляем старые данные (если есть)
Product.objects.all().delete()
Category.objects.all().delete()

# Создаем категории
electronics = Category.objects.create(
    name="Электроника",
    description="Техника и гаджеты"
)
books = Category.objects.create(
    name="Книги",
    description="Печатные издания"
)
clothing = Category.objects.create(
    name="Одежда",
    description="Одежда и аксессуары"
)

print(f"Создано категорий: {Category.objects.count()}")
for cat in Category.objects.all():
    print(f"  - {cat.id}: {cat.name}")

print("\n2. Создание продуктов:")
print("-" * 40)

# Создаем продукты
Product.objects.create(
    name="Смартфон",
    description="Современный смартфон с камерой 48 МП",
    price=29999.99,
    category=electronics
)

Product.objects.create(
    name="Ноутбук",
    description="Игровой ноутбук с видеокартой RTX 4060",
    price=79999.99,
    category=electronics
)

Product.objects.create(
    name="Футболка",
    description="Хлопковая футболка черного цвета",
    price=1999.99,
    category=clothing
)

Product.objects.create(
    name="Книга по Python",
    description="Программирование на Python для начинающих",
    price=2499.99,
    category=books
)

print(f"Создано продуктов: {Product.objects.count()}")

print("\n3. Получить все категории:")
print("-" * 40)
all_categories = Category.objects.all()
for cat in all_categories:
    print(f"  - {cat.id}: {cat.name}")

print("\n4. Получить все продукты:")
print("-" * 40)
all_products = Product.objects.all()
for prod in all_products:
    print(f"  - {prod.id}: {prod.name} - {prod.price} руб. ({prod.category})")

print("\n5. Найти все продукты в категории 'Электроника':")
print("-" * 40)
electronics_products = Product.objects.filter(category=electronics)
for prod in electronics_products:
    print(f"  - {prod.name}: {prod.description[:30]}... - {prod.price} руб.")

print("\n6. Обновить цену продукта:")
print("-" * 40)
smartphone = Product.objects.get(name="Смартфон")
print(f"  Старая цена смартфона: {smartphone.price} руб.")
smartphone.price = 27999.99
smartphone.save()
print(f"  Новая цена смартфона: {smartphone.price} руб.")

print("\n7. Удалить продукт:")
print("-" * 40)
product_to_delete = Product.objects.get(name="Футболка")
print(f"  Удаляем продукт: {product_to_delete.name}")
product_to_delete.delete()
print(f"  Осталось продуктов: {Product.objects.count()}")

print("\n8. Дополнительные запросы:")
print("-" * 40)

# Фильтр по цене
expensive_products = Product.objects.filter(price__gt=20000)
print(f"  Дорогие товары (>20000 руб.): {expensive_products.count()}")

# Сортировка по цене
sorted_products = Product.objects.order_by('-price')
print("  Товары по убыванию цены:")
for prod in sorted_products:
    print(f"    - {prod.name}: {prod.price} руб.")

# Поиск по описанию
python_products = Product.objects.filter(description__icontains='python')
print(f"\n  Товары с 'Python' в описании: {python_products.count()}")

print("\n" + "=" * 60)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("=" * 60)
