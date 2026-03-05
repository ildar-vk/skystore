# catalog/urls.py
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    IndexView, ContactView, ProductListView,
    ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    CategoryListView, ProductUnpublishView,
    CategoryProductsView  # импортируем новое представление
)

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),

    # Продукты
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('products/category/<int:category_id>/', ProductListView.as_view(), name='product_list_by_category'),

    # Новый URL для продуктов по категории (отдельное представление)
    path('category/<int:category_id>/products/', CategoryProductsView.as_view(), name='category_products'),

    # Категории
    path('categories/', CategoryListView.as_view(), name='category_list'),
]