from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Загружает тестовые данные для продуктов и категорий'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Пропустить подтверждение'
        )
    
    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write('=' * 50)
        self.stdout.write('Загрузка тестовых данных...')
        self.stdout.write('=' * 50)
        
        if not force:
            confirm = input("Удалить все существующие данные? (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Отменено.'))
                return
        
        # Удаляем существующие данные
        self.stdout.write('Удаление продуктов...')
        Product.objects.all().delete()
        
        self.stdout.write('Удаление категорий...')
        Category.objects.all().delete()
        
        # Загружаем фикстуры
        fixtures_dir = os.path.join('catalog', 'fixtures')
        
        try:
            # Загружаем категории
            self.stdout.write('Загрузка категорий...')
            category_fixture = os.path.join(fixtures_dir, 'category_data.json')
            if os.path.exists(category_fixture):
                call_command('loaddata', category_fixture)
                self.stdout.write(self.style.SUCCESS('Категории загружены'))
            else:
                self.stdout.write(self.style.WARNING(f'Файл {category_fixture} не найден'))
            
            # Загружаем продукты
            self.stdout.write('Загрузка продуктов...')
            product_fixture = os.path.join(fixtures_dir, 'product_data.json')
            if os.path.exists(product_fixture):
                call_command('loaddata', product_fixture)
                self.stdout.write(self.style.SUCCESS('Продукты загружены'))
            else:
                self.stdout.write(self.style.WARNING(f'Файл {product_fixture} не найден'))
            
            self.stdout.write('=' * 50)
            self.stdout.write(self.style.SUCCESS('✅ Данные успешно загружены!'))
            self.stdout.write('=' * 50)
            
            # Статистика
            self.stdout.write(f'📊 Категорий: {Category.objects.count()}')
            self.stdout.write(f'📊 Продуктов: {Product.objects.count()}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))
