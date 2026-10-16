import pytest
from apps.reservations.models import Reservation
from apps.rooms.models import Room
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_viewsets_rejects_overlap(client):
    #setup/preparation
    room = Room.objects.create(name= "Room A", capacity =5)
    user = User.objects.create_user(username = "sultan",password="sultan1234")


    #Force login so request.user works
    # Force le login pour que request.user marche
    client.force_login(user)

    payload_1 = {
        "room":room.id,
        "start_time":"2026-09-09T09:09:09",
        "end_time":"2026-09-09T12:00:00"
    }
    #first creation
    response_1 = client.post("/api/reservations/v2/",
                             data =payload_1,
                             content_type="application/json")
    assert response_1.status_code == 201 , f"Expected 201, Got {response_1.status_code}:{response_1.content}"

    #overlapping/chauvechement
    payload ={
        "room":room.id,
        "start_time":"2026-09-09T11:00:00",
        "end_time":"2026-09-09T15:00:00"
    }
    response_2= client.post("/api/reservations/v2/",
                            data = payload,
                            content_type="application/json")
    assert response_2.status_code == 400, f"Epected 400, Got :{response_2.status_code}:{response_2.content}"
    print(f"\n Overlapping rejected by serializer : {response_2.json()}")
