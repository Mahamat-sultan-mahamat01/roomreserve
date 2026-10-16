from apps.rooms.models import Room
from .models import Reservation
from rest_framework import serializers


class ReservationSerializer(serializers.ModelSerializer):
    # Explicit fields so we can control validation
    # Champs explicites pour contrôler la validation
    room = serializers.PrimaryKeyRelatedField(queryset =Room.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ["id","room","user","start_time","end_time","status","created_at"]
        read_only_fields =["id","status","created_at"]
    
    def validate(self,attrs):
        """
        Custom validation — runs AFTER field-level validation.
        C'est ici qu'on met les règles métier complexes.
        """
        room = attrs.get("room")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        #Rule 1 stat_time must be before end_time
        if start_time and end_time and (start_time>= end_time):
            raise serializers.ValidationError(
                {"end_time":"end_time must be after start_time!"}
            )
        #no overlapping the same slot in same room
        conflict = Reservation.objects.filter(
            room = room,
            status__in = [Reservation.Status.PENDING, Reservation.Status.CONFIRMED],
            start_time__lt =end_time,
            end_time__gt =start_time
        ).exists()

        if conflict:
            raise serializers.ValidationError(
                {"detail":"This room is already reserved for this time slot. "}
            )
        return attrs