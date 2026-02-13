# catalog/debug_views.py
from django.http import HttpResponse
from .models import Product, Category


def debug_catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Отладка каталога</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            .category { background-color: #f0f0f0; margin: 20px 0; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>🔍 Отладка каталога Skystore</h1>

        <div class="category">
            <h2>📊 Статистика</h2>
            <p>Всего категорий: <strong>""" + str(categories.count()) + """</strong></p>
            <p>Всего товаров: <strong>""" + str(products.count()) + """</strong></p>
        </div>

        <h2>📁 Категории</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Описание</th>
                <th>Кол-во товаров</th>
            </tr>
    """

    for cat in categories:
        cat_products = cat.products.count()
        html += f"""
            <tr>
                <td>{cat.id}</td>
                <td>{cat.name}</td>
                <td>{cat.description or 'Нет описания'}</td>
                <td><strong>{cat_products}</strong></td>
            </tr>
        """

    html += """
        </table>

        <h2>📦 Товары</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Цена</th>
                <th>Категория</th>
                <th>Описание</th>
            </tr>
    """

    for prod in products:
        html += f"""
            <tr>
                <td>{prod.id}</td>
                <td><strong>{prod.name}</strong></td>
                <td>{prod.price} ₽</td>
                <td>{prod.category.name if prod.category else '❌ НЕТ КАТЕГОРИИ'}</td>
                <td>{prod.description[:50] if prod.description else 'Нет'}</td>
            </tr>
        """

    html += """
        </table>

        <h2>🔗 Проверка URL</h2>
        <ul>
            <li><a href="/products/">/products/</a> - список товаров</li>
            <li><a href="/categories/">/categories/</a> - список категорий</li>
            <li><a href="/blog/">/blog/</a> - блог</li>
        </ul>
    </body>
    </html>
    """

    return HttpResponse(html)