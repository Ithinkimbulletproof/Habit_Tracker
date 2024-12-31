import os
import django
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
django.setup()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password123")
