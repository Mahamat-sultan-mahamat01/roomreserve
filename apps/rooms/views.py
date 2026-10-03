from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Room

# Create your views here.
def room_list(request):
    rooms =Room.objects.filter(is_active=True).values('id','name','capacity','location')
    return JsonResponse({"resultant": list(rooms)})
def room_detail(request,pk):
    room = get_object_or_404(Room, pk=pk)
    data = {
        "id":room.id,
        "name":room.name,
        "capacity":room.capacity,
        "is_active":room.is_active
    }
    return JsonResponse(data)