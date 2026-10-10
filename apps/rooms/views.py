from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Room
from django.db.models import Q,Count

# Create your views here.
def room_stat(request):
   #Get 5 high active rooms and their reservations count
   rooms =(
      Room.objects.filter(is_active=True) #just active rooms
      .annotate( #thoses with status pending or confirmed
          total_reservation=Count("reservations",filter=Q(
         reservations__status__in=["pending","confirmed"]
      )))
      .filter(total_reservation__gt=0)
      .order_by("-total_reservation")[:5] #order by total reservation and limit to 5
   )
   #design manual json
   data = [
       {
           "id":room.id,
           "name":room.name,
           "capacity":room.capacity,
           "location":room.location,
           "total_reservation":room.total_reservation
       }
       for room in rooms
   ]
   return JsonResponse({"top_rooms": data})

def room_list(request):
    rooms =Room.objects.filter(is_active=True).values('id','name','capacity','location')
    return JsonResponse({"results": list(rooms)})
def room_detail(request,pk):
    room = get_object_or_404(Room, pk=pk)
    data = {
        "id":room.id,
        "name":room.name,
        "capacity":room.capacity,
        "is_active":room.is_active
    }
    return JsonResponse(data)