from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
        managers_group = Group.objects.create(
            name='Managers'
        )
        view_newsletter_permission = Permission.objects.get(
            codename='view_newsletter'
        )
        view_client_permission = Permission.objects.get(
            codename='view_client'
        )
        view_user_permission = Permission.objects.get(
            codename='view_user'
        )
        block_user_permission = Permission.objects.get(
            codename='block_user'
        )
        stop_newsletter_permission = Permission.objects.get(
            codename='stop_newsletter'
        )

        managers_group.permissions.add(
            view_newsletter_permission,
            view_client_permission, view_user_permission,
            block_user_permission, stop_newsletter_permission
        )
