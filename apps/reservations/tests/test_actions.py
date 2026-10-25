from django.contrib.auth import get_user_model
from apps.reservations.models import Reservation
from apps.rooms.models import Room
import pytest
User = get_user_model()

#pay test
@pytest.mark.django_db
def test_pay_confirmed(client):
    #setup
    user = User.objects.create_user(username="Ali",password="Ali1234")
    other= User.objects.create_user(username="thief",password="thief1234")
    room = Room.objects.create(name="RA",capacity=19)

    #create a reservation with user
    client.force_login(user)
    payload = {
        "room":room.id,
        "start_time":"2026-09-09T12:00:00",
        "end_time":"2026-09-09T13:00:00"
    }
    response = client.post("/api/reservations/v2/",
                           data =payload,
                           content_type="application/json")
    assert response.status_code ==201, f"Got:{response.status}:{response.content}"
    res_id = response.json()["id"]
    assert response.json()["status"] =="pending"

    #user try to pay
    res_pay = client.post(f"/api/reservations/v2/{res_id}/pay/")
    assert res_pay.status_code == 200 , f"Got: {res_pay.status_code}:{res_pay.content}"
    assert Reservation.objects.get(id=res_id).status =="confirmed"
    print(f"\nPayment confirms the reservation.")

    #other user try
    client.force_login(other)
    forbidden = client.post(f"/api/reservations/v2/{res_id}/pay/")
    assert forbidden.status_code == 403 ,(f"Got : {forbidden.status_code}:{forbidden.content}")
    print("\n other cannot pay sameone's reservation:")

    #try again
    resp_again = client.post(f"/api/reservations/v2/{res_id}/pay/")
    assert resp_again.status_code == 403, f"{resp_again.status_code}:{resp_again.content}"




                               


@pytest.mark.django_db
def test_cancel_own_reservation(client):
    #Setup
    room=Room.objects.create(name="Room 21",capacity=12)
    user= User.objects.create_user(username="sultan",password="sultan1234")
    other_user = User.objects.create_user(username="otheruser",password="test1234")
    client.force_login(user)
    #create the reservation
    payload = {
        "room":room.id,
        "start_time":"2020-12-12T12:00:00",
        "end_time":"2020-12-12T14:00:00"
    }
    response = client.post("/api/reservations/v2/",
                             data = payload,
                             content_type="application/json")
    assert response.status_code == 201, (f"Creation failed, status:{response.status_code}:Body {response.content}")

    res_id =response.json()["id"]

    #cancel your own reservation
    cancel_response = client.post(f"/api/reservations/v2/{res_id}/cancel/")
    assert cancel_response.status_code == 200,(f"{cancel_response.status_code}:{cancel_response.content}")
    assert Reservation.objects.get(id=res_id).status == "cancelled"
    print(f"\nOwn reservation cancelled successfully.")

    #cancel again
    cancel_again = client.post(f"/api/reservations/v2/{res_id}/cancel/")
    assert cancel_again.status_code == 400,(f"{cancel_again.status_code}:{cancel_again.content}")
    print(f"\n Cannot cancelled it was cancelled!")

    #try to cancelled to other
    #create new reservation 
    client.force_login(other_user)
    payload ={
        "room":room.id,
        "start_time":"2026-06-06T10:00:00",
        "end_time":"2026-06-06T11:00:00"
    }
    resp_2 = client.post("/api/reservations/v2/",
                         data = payload,
                         content_type="application/json")
    assert resp_2.status_code ==201, f"other created : {resp_2.status_code}:{resp_2.content}"
    resid2 = resp_2.json()["id"]
    #try to connect with user
    client.force_login(user)
    forbidden = client.get(f"/api/reservations/v2/{resid2}/cancel/")
    assert forbidden.status_code == 403
    print(f"\n Cannot cancelled sameone else's reservation!")



  
    
