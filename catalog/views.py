from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    """Главная страница - список всех продуктов"""
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Страница контактов"""
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    """Страница одного товара"""
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'title': product.name
    }
    return render(request, 'catalog/product_detail.html', context)
