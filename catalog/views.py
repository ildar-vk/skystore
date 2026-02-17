# catalog/views.py (полная версия)
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm


# 🔥 ДОБАВИТЬ: Главная страница
class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


# 🔥 ДОБАВИТЬ: Страница контактов
class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


# 🔥 ДОБАВИТЬ: Список продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = Category.objects.all()
        return context


# 🔥 ДОБАВИТЬ: Детальная информация о продукте
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# У вас уже есть:
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Продукт успешно создан!')
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, '✅ Продукт успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '❌ Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


# У вас уже есть:
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, '✅ Продукт успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '❌ Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


# У вас уже есть:
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '✅ Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


# 🔥 ДОБАВИТЬ: Список категорий
class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context