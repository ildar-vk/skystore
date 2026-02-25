# users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class UserRegistrationView(CreateView):
    """
    Контроллер регистрации пользователя
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        """
        Действия при успешной валидации формы
        """
        # Сохраняем пользователя
        response = super().form_valid(form)

        # Отправляем приветственное письмо
        self.send_welcome_email(form.cleaned_data['email'])

        # Автоматически логиним пользователя после регистрации
        user = form.save()
        auth_login(self.request, user)

        messages.success(
            self.request,
            '✅ Регистрация прошла успешно! Добро пожаловать!'
        )
        return response

    def form_invalid(self, form):
        """
        Действия при невалидной форме
        """
        print("=" * 50)
        print("FORM INVALID - ОШИБКИ РЕГИСТРАЦИИ:")
        print("Email:", form.data.get('email', 'не указан'))
        print("Ошибки:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        print("=" * 50)

        error_messages = []
        for field, errors in form.errors.items():
            field_name = dict(form.fields)[field].label if field in form.fields else field
            for error in errors:
                error_messages.append(f"{field_name}: {error}")

        messages.error(
            self.request,
            '❌ Ошибка регистрации:\n' + '\n'.join(error_messages)
        )
        return super().form_invalid(form)

    def send_welcome_email(self, email):
        """
        Отправка приветственного письма
        """
        subject = 'Добро пожаловать в Skystore!'
        message = f'''
        Здравствуйте!

        Благодарим вас за регистрацию в нашем магазине Skystore.

        Теперь вы можете:
        ✅ Просматривать каталог товаров
        ✅ Создавать свои товары
        ✅ Оставлять отзывы
        ✅ Участвовать в акциях

        С уважением,
        Команда Skystore
        '''

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Логируем ошибку, но не прерываем регистрацию
            print(f"Ошибка отправки письма: {e}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserLoginView(LoginView):
    """
    Контроллер авторизации пользователя
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:index')

    def form_valid(self, form):
        messages.success(self.request, '✅ Вы успешно вошли в систему!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            '❌ Неправильный email или пароль. Попробуйте снова.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        return context


class UserProfileView(TemplateView):
    """
    Контроллер просмотра профиля пользователя
    """
    template_name = 'users/profile.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Проверка авторизации
        """
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста, войдите в систему для просмотра профиля.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'
        context['user'] = self.request.user
        return context


def logout_view(request):
    """
    Контроллер выхода из системы
    """
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, '👋 Вы вышли из системы. До свидания!')
    return redirect('catalog:index')