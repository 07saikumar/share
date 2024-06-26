from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    expiry_time = models.DurationField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.creation_time + self.expiry_time

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    expiry_time = models.DurationField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.creation_time + self.expiry_time
