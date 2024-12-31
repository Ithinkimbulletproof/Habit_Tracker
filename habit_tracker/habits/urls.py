from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitListView, UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/public-habits/', PublicHabitListView.as_view(), name='public-habits'),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
