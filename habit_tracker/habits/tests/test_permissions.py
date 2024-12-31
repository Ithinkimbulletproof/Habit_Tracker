import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

@pytest.mark.django_db
def test_user_can_edit_own_habit(api_client, user):
    habit = Habit.objects.create(
        user=user,
        place="Дом",
        time="08:00:00",
        action="Утренняя зарядка",
        pleasant_habit=True,
        execution_time=60,
    )
    api_client.login(username="testuser", password="password123")
    response = api_client.patch(f"/api/habits/{habit.id}/", {"action": "Вечерняя зарядка"})
    assert response.status_code == 200
    habit.refresh_from_db()
    assert habit.action == "Вечерняя зарядка"

@pytest.mark.django_db
def test_user_cannot_edit_others_habit(api_client, user):
    another_user = User.objects.create_user(username="anotheruser", password="password123")
    habit = Habit.objects.create(
        user=another_user,
        place="Дом",
        time="08:00:00",
        action="Утренняя зарядка",
        pleasant_habit=True,
        execution_time=60,
    )
    api_client.login(username="testuser", password="password123")
    response = api_client.patch(f"/api/habits/{habit.id}/", {"action": "Вечерняя зарядка"})
    assert response.status_code == 403
