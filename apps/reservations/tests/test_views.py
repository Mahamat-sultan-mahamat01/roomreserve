import json
from django.contrib.auth import get_user_model
from apps.rooms.models import Room
User = get_user_model()
import pytest
@pytest.mark.django_db
def test_reservation_conflict(client):
    room = Room.objects.create(name="Test_room",capacity=10)
    user = User.objects.create_user(username="sultany",password="sultany123")
    payload_1={
        "user_id": user.id,
        "room_id": room.id,
        "start_time":"2023-03-15T10:10:00",
        "end_time":"2023-03-16T10:00:00"
    }
    response_1 = client.post("/api/reservations/create/",
                             data =json.dumps(payload_1),
                             content_type="application/json")
    assert response_1.status_code ==201 ,f" Expected 201 got {response_1.status_code} :{response_1.content}"

    payload_2 = {
        "user_id":user.id,
        "room_id":room.id,
        "start_time":"2023-03-16T09:10:10",
        "end_time":"2023-03-17T11:10:10"

    }
    response_2 =client.post("/api/reservations/create/",
                            data =json.dumps(payload_2),
                            content_type = "application/json")
    assert response_2.status_code ==409, f"expected 409 overloapping should be rejected! {response_2.status_code}"
    print(f"STATUS:{response_2.status_code}")
    print(f"jsons files: {response_2.json()}")
    payload_3 = {
        "user_id":user.id,
        "room_id":room.id,
        "start_time":"2023-04-04T12:00:00",
        "end_time":"2023-04-04T13:00:00"
    }
    response_3 = client.post("/api/reservations/create/",
                             data =json.dumps(payload_3),
                             content_type = "application/json")
    assert response_3.status_code == 201, f"expected 201 got {response_3.status_code}:{response_3.content}"

#the where the end_time before start_time
@pytest.mark.django_db
def test_reservation_rejects_end_before_start(client):
    room = Room.objects.create(name="Test_Room",capacity=7)
    user = User.objects.create_user(username="sultany",password="sultany123")
    payload ={
        "room_id":room.id,
        "user_id":user.id,
        "start_time":"2000-10-10T10:00:00",
        "end_time": "2000-10-10T09:00:00"
    }
    response = client.post("/api/reservations/create/",
                           data =json.dumps(payload),
                           content_type ="application/json")
    assert response.status_code == 400 ,f" 400,got {response.status_code}:{response.content}"

    #invalid client
@pytest.mark.django_db
def test_cancelled_reservation_frees_slot(client):
   room = Room.objects.create(name="T1",capacity=17)
   user= User.objects.create_user(username="Ali",password="Ali&é")
   payloa_4 ={
       "user_id":user.id,
       "room_id":room.id,
       "start_time":"2020-02-02T12:00:00",
       "end_time":"2020-02-02T17:00:00"
   }
   res_4 = client.post("/api/reservations/create/",
                       data = json.dumps(payloa_4),
                       content_type="application/json")
   assert res_4.status_code == 201 , f"\nretry again is success: {res_4.status_code}:{res_4.content}"
   from apps.reservations.models import Reservation
   res = Reservation.objects.get(id = res_4.json()['id'])
   res.status ="cancelled"
   res.save()
   print( f"\ncancelled success")
   res_5 =client.post("/api/reservations/create/",
                      data =json.dumps(payloa_4),
                      content_type = "application/json")
   assert res_5.status_code == 201 , f"\nretry again is very success{res_5.status_code}:{res_5.content}"
