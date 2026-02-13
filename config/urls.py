from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog.debug_views import debug_catalog  # Добавьте этот импорт

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blog/', include('blog.urls')),
    path('debug/', debug_catalog, name='debug'),  # Добавьте эту строку
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)