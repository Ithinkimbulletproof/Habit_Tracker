import pytest
from django.core.exceptions import ValidationError
from habits.models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_execution_time_validation():
    user = User.objects.create_user(username="testuser", password="password123")
    habit = Habit(
        user=user,
        place="Дом",
        time="08:00:00",
        action="Утренняя зарядка",
        pleasant_habit=True,
        execution_time=150,
    )
    with pytest.raises(ValidationError) as excinfo:
        habit.clean()
    assert "Время выполнения не может быть больше 120 секунд." in str(excinfo.value)
