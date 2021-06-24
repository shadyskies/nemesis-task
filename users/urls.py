from django.urls import path
from .views import RegisterView, ProfileView, LoginView, ProfileEditView, ProfileClearAttr, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<str:key>', ProfileEditView().as_view(), name='profile-edit'),
    path('profile/delete/<str:key>', ProfileClearAttr().as_view(), name='profile-delete'),
]