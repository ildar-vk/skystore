# catalog/services.py
from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id):
    """
    Возвращает queryset опубликованных продуктов в указанной категории.
    """
    return Product.objects.filter(
        category_id=category_id,
        is_published=True
    ).select_related('category', 'owner').order_by('-created_at')