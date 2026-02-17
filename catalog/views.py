from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm  # Импортируем форму


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm  # Используем нашу кастомную форму
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm  # Используем нашу кастомную форму
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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '✅ Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)