from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "pleasant_habit",
            "related_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
        ]
        read_only_fields = ["id", "user"]


class UserSerializer(serializers.ModelSerializer):
    habits = serializers.PrimaryKeyRelatedField(many=True, queryset=Habit.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "password", "telegram_id", "habits"]
        extra_kwargs = {
            "password": {"write_only": True},
            "telegram_id": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        habits = validated_data.pop("habits", [])
        user = User.objects.create_user(**validated_data)
        for habit in habits:
            habit.user = user
            habit.save()
        return user
