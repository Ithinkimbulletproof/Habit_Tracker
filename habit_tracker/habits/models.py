from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=255, blank=True, null=True, help_text="Telegram ID пользователя.")

class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255, help_text="Место выполнения привычки.")
    time = models.TimeField(help_text="Время выполнения привычки.")
    action = models.CharField(max_length=255, help_text="Действие привычки.")
    pleasant_habit = models.BooleanField(default=False, help_text="Приятная привычка.")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        help_text="Связанная привычка (только для полезных привычек).",
    )
    periodicity = models.PositiveIntegerField(
        default=7, help_text="Периодичность выполнения привычки в днях."
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Вознаграждение за выполнение привычки.",
    )
    execution_time = models.PositiveIntegerField(
        help_text="Время на выполнение в секундах."
    )
    is_public = models.BooleanField(default=False, help_text="Привычка доступна всем.")

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Выберите либо вознаграждение, либо связанную привычку, но не оба варианта."
            )

        if self.execution_time > 120:
            raise ValidationError("Время выполнения не может быть больше 120 секунд.")

        if self.related_habit and not self.related_habit.pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if self.periodicity < 7:
            raise ValidationError(
                "Периодичность выполнения не может быть меньше 7 дней."
            )

    def __str__(self):
        return f"{self.action} ({'Приятная' if self.pleasant_habit else 'Полезная'})"
