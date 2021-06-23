from django.urls import path
from .views import RegisterView, ProfileView, LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path('register/', register, name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]