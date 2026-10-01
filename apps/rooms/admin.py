from django.contrib import admin
from .models import Room
# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','capacity','location','is_active')
    search_fields = ('name','location')
    list_filter = ('is_active','capacity')
