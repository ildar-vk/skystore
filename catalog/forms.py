# catalog/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Константа с запрещенными словами
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена',
        }
        help_texts = {
            'name': 'Введите название продукта',
            'price': 'Введите цену в рублях',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация будет добавлена позже в задании 3

    def clean_name(self):
        """Валидация поля name на запрещенные слова"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f'Название продукта не может содержать слово "{word}". '
                        f'Пожалуйста, уберите это слово из названия.'
                    )
        return name

    def clean_description(self):
        """Валидация поля description на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise ValidationError(
                        f'Описание продукта не может содержать слово "{word}". '
                        f'Пожалуйста, уберите это слово из описания.'
                    )
        return description

    def clean_price(self):
        """Валидация поля price - цена не может быть отрицательной"""
        price = self.cleaned_data.get('price')

        if price is None:
            raise ValidationError('Пожалуйста, укажите цену продукта.')

        if price < 0:
            raise ValidationError(
                'Цена продукта не может быть отрицательной. '
                'Пожалуйста, укажите корректную цену.'
            )

        if price == 0:
            raise ValidationError(
                'Цена продукта не может быть равной нулю. '
                'Если товар бесплатный, укажите цену 0.01 или обратитесь к администратору.'
            )

        # Можно добавить проверку на максимальную цену
        if price > 1000000:
            raise ValidationError(
                'Цена продукта не может превышать 1 000 000 рублей. '
                'Для указания большей цены обратитесь к администратору.'
            )

        return price

    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')

        # Можно добавить дополнительные проверки, если нужно
        if name and description:
            # Проверка, что название и описание не слишком похожи
            if name.lower() in description.lower():
                # Это просто предупреждение, не ошибка
                from django.contrib import messages
                self.add_error(None,
                               'Описание очень похоже на название. Рекомендуется сделать описание более подробным.')

        return cleaned_data