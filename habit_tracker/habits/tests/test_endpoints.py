import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        place="Дом",
        time="08:00:00",
        action="Утренняя зарядка",
        pleasant_habit=True,
        execution_time=60,
    )

@pytest.mark.django_db
def test_habit_list(api_client, user, habit):
    api_client.login(username="testuser", password="password123")
    response = api_client.get("/api/habits/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["action"] == "Утренняя зарядка"

@pytest.mark.django_db
def test_create_habit(api_client, user):
    api_client.login(username="testuser", password="password123")
    data = {
        "place": "Офис",
        "time": "12:00:00",
        "action": "Обеденный перерыв",
        "pleasant_habit": True,
        "execution_time": 30,
    }
    response = api_client.post("/api/habits/", data)
    assert response.status_code == 201
    assert Habit.objects.filter(action="Обеденный перерыв").exists()
