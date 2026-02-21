# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )
    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    phone_number = forms.CharField(
        label='Номер телефона',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (XXX) XXX-XX-XX'
        })
    )
    country = forms.CharField(
        label='Страна',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу страну'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name',
                  'last_name', 'phone_number', 'country')

    def clean_email(self):
        """
        Проверка уникальности email
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_phone_number(self):
        """
        Валидация номера телефона (опционально)
        """
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Удаляем все символы кроме цифр и +
            cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            if len(cleaned_phone) < 10:
                raise ValidationError('Введите корректный номер телефона')
        return phone

    def save(self, commit=True):
        """
        Сохранение пользователя
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.country = self.cleaned_data.get('country', '')

        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя
    """
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )