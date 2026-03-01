# catalog/views.py
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Product, Category
from .forms import ProductForm


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Показываем только опубликованные продукты всем
        queryset = queryset.filter(is_published=True)

        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        # Владелец и модератор видят все, остальные только опубликованные
        if self.request.user.is_authenticated:
            if (self.request.user.is_superuser or
                    self.request.user.has_perm('catalog.can_unpublish_product')):
                return Product.objects.all()

        return Product.objects.filter(is_published=True)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        # Автоматически устанавливаем владельца
        form.instance.owner = self.request.user
        messages.success(self.request, '✅ Продукт успешно создан!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        """Проверка прав на редактирование"""
        product = self.get_object()
        user = self.request.user

        # Суперпользователь или владелец могут редактировать
        return user.is_superuser or product.owner == user

    def handle_no_permission(self):
        messages.error(self.request, '❌ У вас нет прав на редактирование этого продукта')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def form_valid(self, form):
        messages.success(self.request, '✅ Продукт успешно обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        """Проверка прав на удаление"""
        product = self.get_object()
        user = self.request.user

        # Могут удалять:
        # 1. Суперпользователь
        # 2. Владелец продукта
        # 3. Модератор с правом удаления любого продукта
        return (user.is_superuser or
                product.owner == user or
                user.has_perm('catalog.can_delete_any_product'))

    def handle_no_permission(self):
        messages.error(self.request, '❌ У вас нет прав на удаление этого продукта')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '✅ Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Отмена публикации продукта (только для модераторов)"""
    model = Product
    fields = ['is_published']
    template_name = 'catalog/product_unpublish.html'
    permission_required = 'catalog.can_unpublish_product'

    def form_valid(self, form):
        form.instance.is_published = False
        messages.success(self.request, '✅ Публикация продукта отменена')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context