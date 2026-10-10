from django.shortcuts import render
import json
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Reservation
from apps.rooms.models import Room


User = get_user_model()
@require_http_methods(['GET']) #mean only get method is allowed
def reservation_list(request):
    reservation = Reservation.objects.select_related('room', 'user').values(
        'id','room__name','user__username','status','start_time','end_time'
    )
    return JsonResponse({"result":list(reservation)})


@csrf_exempt # This view is exempt from CSRF verification
@require_http_methods(['POST']) # mean only post method is allowed
def reservation_create(request):
    payload = json.loads(request.body) # parse the JSON payload of load the data
    room = Room.objects.get(pk=payload['room_id']) # get the room object based on the room_id in the payload
    user = User.objects.get(pk=payload['user_id']) # get the user object based on the user_id in the payload
    start_time = timezone.make_aware(datetime.fromisoformat(payload['start_time'])) # convert the start_time string to a datetime object
    end_time = timezone.make_aware(datetime.fromisoformat(payload['end_time'])) # convert the end_time string to a datetime object

    if start_time >= end_time:
        return JsonResponse({"error":"start_time must be before end_time"},status=400)
    
    #conflict bug
    conflict = Reservation.objects.filter(
        room = room, # The room being reserved
        status__in = [Reservation.Status.PENDING, Reservation.Status.CONFIRMED], # The statuses to check for conflicts
        start_time__lt = end_time, # The start time must be before the end time
        end_time__gt = start_time # The end time must be after the start time

    ).exists() # Check if any conflicting reservations exist

    if conflict:
        return JsonResponse({"error":"The room is already reserved for the selected time period."},status=409)
    reservation = Reservation.objects.create(
        room = room, # The room being reserved
        user = user, # The user making the reservation
        start_time = start_time, # The start time of the reservation
        end_time = end_time # The end time of the reservation
    )
    return JsonResponse({
        "id":reservation.id,
        "room":room.name, # The name of the room being reserved
        "user":user.username, # The username of the user making the reservation
        "status":reservation.status, #The status of reservation
        "start_time":reservation.start_time,
        "end_time":reservation.end_time
   
    },status=201) # Return a 201 Created status code
    





