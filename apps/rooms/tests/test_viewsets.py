import pytest
from apps.rooms.models import Room
@pytest.mark.django_db
def test_viewset_create_room(client):
    payload = {"name":"Viewset Room","capacity":10,"location":"ChadOne1"}
    response = client.post("/api/rooms/v2/",
                           data = payload,
                           content_type ="application/json")
    assert response.status_code == 201, f"Got :{response.status_code}:{response.content}"
    assert Room.objects.filter(name ="Viewset Room").exists()
    print(f"\n Viewset created room : {response.json()}")

#rejected 
@pytest.mark.django_db
def test_viewset_rejects_invalid_data(client):
    payload = {"name":"","capacity":-5}
    response = client.post("/api/rooms/v2/",
                           data = payload,
                           content_type="application/json")
    assert response.status_code == 400 ,f"Got: {response.status_code}:{response.content}"
    errors = response.json()
    assert "name" in errors 
    assert "capacity" in errors
    print(f"\nErrors validations : {errors}")