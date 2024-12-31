from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Habit
from .serializers import HabitSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
