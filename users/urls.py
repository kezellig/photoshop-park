from django.urls import path
from django.contrib.auth import views as auth_view
from users.views import register, profile, signin

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/<slug:username>', profile, name='profile')
]