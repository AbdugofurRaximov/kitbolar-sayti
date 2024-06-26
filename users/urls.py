from django.urls import path
from .views import RegisterView, LoginView,ProfileView,LogoutView,ProfileEditView


app_name = "users"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(),name='profile'),
    path('profile/edit/', ProfileEditView.as_view(),name='profile-edit')
]