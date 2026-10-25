from django.shortcuts import render
import json
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from .models import Reservation
from apps.rooms.models import Room
from rest_framework import viewsets, permissions,status
from rest_framework.response import Response
from .serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("room","user").all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["room","status","user"]
    ordering_fields = ["start_time","end_time","created_at"]

    #auto user connect current
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    #pay simule to confirm
    """
         1 Seul le propriétaire peut payer	403 Forbidden
        2	On ne peut payer qu'une résa pending	400 Bad Request
        3	Une fois payée, elle est confirmed	200 OK
        4	On ne peut pas payer une résa cancelled	400 Bad Request
        POST: /api/reservations/v2/{id}/pay/
    """
    @action(detail=True, methods=["post"])
    def pay(self,request, pk=None):
        #check it is itself user propriataire
        reservation = self.get_object()
        if reservation.user!=request.user:
            return Response(
                {"error":"You can pay Only your own reservation!"},
                status = status.HTTP_403_FORBIDDEN,
            )
        #check stat of status only pending can 
        if reservation.status!=Reservation.Status.PENDING:
            return Response(
                {"error":"Cannot pay a reservation with this status:{reservation.status}!"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        reservation.status=Reservation.Status.CONFIRMED
        reservation.save()
        return Response(
            {"message":"Payment successfully. reservation confirmed:status:{reservation.status}"},
            status = status.HTTP_200_OK,
        )
        
    #cancel
    @action(detail=True, methods =["post"])
    def cancel(self,request,pk=None):
        reservation = self.get_object()
        #check is same users
        if reservation.user!=request.user:
            return Response(
                {"error":"You can only cancel your own reservation!"},
                status = status.HTTP_403_FORBIDDEN,
            )
        #again impossible ,if status was cancelled 
        if reservation.status  == Reservation.Status.CANCELLED:
            return Response(
                {"error":"Reservation is  already cancelled"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        #action
        reservation.status = Reservation.Status.CANCELLED
        reservation.save()
        return Response(
            {"message":"cancelled successfuly!","status":reservation.status},
            status = status.HTTP_200_OK,
        )

        

   

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
    





