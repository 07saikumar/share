from django.core.management.base import BaseCommand
from content.models import Room
from django.utils import timezone
from django.db.models import F

class Command(BaseCommand):
    help = 'Expire rooms that have passed their expiry time'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_rooms = Room.objects.filter(creation_time__lt=now - F('expiry_time'))
        expired_count = expired_rooms.count()
        expired_rooms.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully expired {expired_count} rooms'))
