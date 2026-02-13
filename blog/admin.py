from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at')
    list_editable = ('is_published',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content')
        }),
        ('Изображение', {
            'fields': ('preview',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('is_published', 'views_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )