from django.conf import settings
from django.db import models
from apps.rooms.models import Room

# Create your models here.
class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PE",('pending')
        CONFIRMED = 'CO',('confirmed')
        CANCELLED = 'CA',('cancelled')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20,choices=Status.choices,
                              default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.room.name} {self.start_time:%Y-%m-%d %H:%M}"
   
    
