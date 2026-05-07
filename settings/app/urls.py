from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('users_list/', UserProfileListAdminAPIView.as_view(), name='user_list_admin'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_view'),
    path('cifar_10/', CIFAR10APIView.as_view(), name='cifar_10_view'),
    path('cifar_100/', CIFAR100APIView.as_view(), name='cifar_100_view'),
    path('phones/', SmartphonesAPIView.as_view(), name='smartphones_view')
]