from catalog.models import Category, Product

# Создаем категории если их нет
if not Category.objects.exists():
    Category.objects.create(name="Электроника", description="Техника и гаджеты")
    Category.objects.create(name="Книги", description="Печатные издания")
    Category.objects.create(name="Одежда", description="Одежда и аксессуары")
    print("Категории созданы")

# Создаем тестовые продукты
electronics = Category.objects.get(name="Электроника")
books = Category.objects.get(name="Книги")
clothing = Category.objects.get(name="Одежда")

products_data = [
    {
        'name': 'Смартфон iPhone 15 Pro',
        'description': 'Новейший смартфон Apple с камерой 48 МП, процессором A17 Pro и дисплеем Super Retina XDR. Идеальный выбор для тех, кто ценит качество и производительность.',
        'price': 99999.99,
        'category': electronics
    },
    {
        'name': 'Игровой ноутбук ASUS ROG',
        'description': 'Мощный игровой ноутбук с процессором Intel Core i9, видеокартой NVIDIA RTX 4080 и дисплеем 240 Гц. Побеждайте в любых играх с максимальными настройками графики.',
        'price': 199999.99,
        'category': electronics
    },
    {
        'name': 'Книга "Чистый код"',
        'description': 'Классическая книга Роберта Мартина о том, как писать качественный код. Обязательна к прочтению каждому программисту.',
        'price': 2499.99,
        'category': books
    },
    {
        'name': 'Футболка хлопковая',
        'description': 'Мужская хлопковая футболка премиального качества. Доступна в различных цветах. Идеально подходит для повседневной носки.',
        'price': 1999.99,
        'category': clothing
    },
    {
        'name': 'Наушники Sony WH-1000XM5',
        'description': 'Беспроводные наушники с активным шумоподавлением. Лучшее качество звука на рынке. Автономность до 30 часов.',
        'price': 34999.99,
        'category': electronics
    },
    {
        'name': 'Книга "Грокаем алгоритмы"',
        'description': 'Иллюстрированное руководство по алгоритмам для начинающих. Сложные концепции объясняются простым языком с помощью иллюстраций.',
        'price': 1899.99,
        'category': books
    }
]

for product_data in products_data:
    Product.objects.create(**product_data)

print(f"Создано продуктов: {Product.objects.count()}")
print("Тестовые данные добавлены успешно!")
