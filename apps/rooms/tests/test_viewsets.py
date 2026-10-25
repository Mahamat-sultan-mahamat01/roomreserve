import pytest
from apps.rooms.models import Room
from django.contrib.auth import get_user_model
User = get_user_model()



@pytest.mark.django_db
def test_viewset_filter_by_capacity(client):
    Room.objects.create(name="Big",capacity="20")
    Room.objects.create(name="Small",capacity="5")
    
    response =client.get("/api/rooms/v2/?capacity=5")
    data = response.json()
    assert  data["count"] ==1
    assert data["results"][0]["name"]=="Small"
    print(f"\n filter by capacity wokrs: {data["results"]}")

@pytest.mark.django_db
def test_viewset_search_by_name(client):
    Room.objects.create(name="Meeting Alpha",capacity=10)
    Room.objects.create(name="Meeting Lammda",capacity=10)
    response =client.get("/api/rooms/v2/?search=Alpha")
    data = response.json()
    assert data["count"]==1
    assert "Alpha"in data["results"][0]["name"]
    print(f"\n Search works: {data["results"]}")
#paginations
@pytest.mark.django_db
def test_viewset_pagination(client):
    for i in range(15):
        Room.objects.create(name=f"Room {i:02d}", capacity=5)
        response = client.get("/api/rooms/v2/")
        assert response.status_code  == 200
        data = response.json()

    #check pagination keys
    assert "count" in data
    assert "next" in data 
    assert "previous" in data
    assert "results" in data


    #page has exactly 10
    assert data["count"] ==15
    assert len(data["results"]) == 10
    assert data["next"] is not None
    assert data["previous"] is None
    print(f"\n Paginated : {data["count"]},total , {len(data["results"])}, on page 1")
    print(f"\n Next URL page : {data["next"]}")

@pytest.mark.django_db
def test_viewset_create_room(client):
    user = User.objects.create_user(username="creator2",password="creator2")
    client.force_login(user)

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
    user = User.objects.create_user(username="creator",password="creator1234")
    client.force_login(user)

    payload = {"name":"","capacity":-5}
    response = client.post("/api/rooms/v2/",
                           data = payload,
                           content_type="application/json")
    assert response.status_code == 400 ,f"Got: {response.status_code}:{response.content}"
    errors = response.json()
    assert "name" in errors 
    assert "capacity" in errors
    print(f"\nErrors validations : {errors}")