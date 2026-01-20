from django.shortcuts import render

from django.shortcuts import render


def home(request):
    """Контроллер главной страницы"""
    return render(request, 'catalog/home.html')


def contacts(request):
    """Контроллер страницы контактов"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику обработки формы
        # Например, сохранение в базу данных или отправка email
        print(f'Новое сообщение от {name} ({phone}): {message}')

    return render(request, 'catalog/contacts.html')
