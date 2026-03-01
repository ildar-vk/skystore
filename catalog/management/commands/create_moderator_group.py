# catalog/management/commands/create_moderator_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов с необходимыми правами'

    def handle(self, *args, **options):
        self.stdout.write('Создание группы модераторов...')

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа создана'))
        else:
            self.stdout.write('Группа уже существует, обновляем права')

        # Получаем нужные разрешения
        permissions = [
            Permission.objects.get(
                content_type=content_type,
                codename='can_unpublish_product'
            ),
            Permission.objects.get(
                content_type=content_type,
                codename='can_delete_any_product'
            ),
            Permission.objects.get(
                content_type=content_type,
                codename='delete_product'  # Стандартное право на удаление
            ),
        ]

        # Добавляем разрешения группе
        moderator_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f'Группе "{moderator_group.name}" назначены права:\n'
                f'- Может отменять публикацию\n'
                f'- Может удалять любой продукт'
            )
        )