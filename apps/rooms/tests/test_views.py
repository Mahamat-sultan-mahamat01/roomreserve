from apps.rooms.models import Room
import pytest
from apps.reservations.models import Reservation
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
User = get_user_model()


@pytest.mark.django_db
def test_room_list(client):
    Room.objects.create(name="Test_Room",capacity=7)
    response = client.get("/api/rooms/")
    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]['name'] =="Test_Room"
    print(f"\nStatus: {response.status_code}")
    print(f"\nBody : {response.json()}")
       
@pytest.mark.django_db
def test_detail_room_not_found(client):
    res= client.get("/api/rooms/9999/")
    assert res.status_code == 404 , f"\n 404  got not 999 {res.status_code}:{res.content}"

 

@pytest.mark.django_db
def test_rooms_list_excludes_inactive(client):
    #create two rooms 
    Room.objects.create(name ="Active room",capacity=5,is_active=True)
    Room.objects.create(name = "Hidden room",capacity=5,is_active=False)
    #get address and translate to json
    response = client.get("/api/rooms/")
    data = response.json()
    #loop in data name
    names =[r["name"] for r in data["results"]]
    assert "Active room" in names, f"Active room should be listed got: {names}"
    assert "Hidden room" not  in names, f"Inactive room should be hidden got: {names}"
    print(f"\nRoom list filtered correctly: {names}")


@pytest.mark.django_db
def test_stats_excludes_empty_rooms(client):
    book_end = Room.objects.create(name ="backend",capacity=3, is_active =True)
    Room.objects.create(name = "U1",capacity =6)
    user = User.objects.create_user(username="Ali", password="ali12")
    #Give book_end a reservation
    Reservation.objects.create(
        user =user,
        room = book_end,
        start_time= timezone.make_aware(datetime.fromisoformat("2026-02-06T10:00:00")),
        end_time= timezone.make_aware(datetime.fromisoformat("2026-02-09T15:12:12"))
    )
    #get stats 
    response = client.get("/api/rooms/stats/")
    data = response.json()
    names =[r["name"] for r in data["top_rooms"]]
    assert "backend" in names , f"Backend room should be listed got : {names}"
    assert "U1" not in names , f" empty room should be hidden got : {names}"
    print(f"\n  Stats filtered correctly: {names}")

