import pytest
from apps.rooms.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_jwt_token_obtain(client):
    """Test that we can get a JWT token by sending credentials."""
    User.objects.create_user(username="jwtuser",password="test1234")
    response = client.post("/api/token/",
                           data = {"username":"jwtuser","password":"test1234"},
                           content_type="application/json")
    assert response.status_code ==200, f"Got:{response.status_code}:{response.content}"
    data =response.json()
    assert "access" in data
    assert "refresh" in data
    print(f"\n Got access in token: {data["access"][:50]}...")

