from django.core.management.base import BaseCommand
from content.models import Room
from django.db.models import Count

class Command(BaseCommand):
    help = 'Remove duplicate rooms'

    def handle(self, *args, **kwargs):
        duplicates = Room.objects.values('room_name').annotate(name_count=Count('room_name')).filter(name_count__gt=1)
        for duplicate in duplicates:
            rooms = Room.objects.filter(room_name=duplicate['room_name'])
            # Keep the first room and delete the rest
            for room in rooms[1:]:
                room.delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate rooms'))
