from django.urls import path
from .views import (
    IndexView, ContactView, ProductListView,
    ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    CategoryListView
)

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),

    # Продукты
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/category/<int:category_id>/', ProductListView.as_view(), name='product_list_by_category'),

    # Категории
    path('categories/', CategoryListView.as_view(), name='category_list'),
]