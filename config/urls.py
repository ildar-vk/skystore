from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Добавляем этот импорт
from catalog.debug_views import debug_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blog/', include('blog.urls')),
    path('debug/', debug_catalog, name='debug'),

    # Добавляем URLs для аутентификации
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)