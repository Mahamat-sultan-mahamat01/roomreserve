from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200,unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name ="Room"
        verbose_name_plural = "Rooms"
    def __str__(self):
        return f"{self.name} - {self.capacity}"
  