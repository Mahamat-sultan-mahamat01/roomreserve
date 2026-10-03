from django.contrib import admin
from .models import Reservation

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room','user','start_time','end_time','status','created_at')
    search_fields = ('room','status')
    date_hierarchy = 'start_time'