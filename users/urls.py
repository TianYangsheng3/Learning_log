"""define url of users"""

from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    # home
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='learning_logs/index.html'),name='logout'),
    path('register/', views.register,name = 'register'),

    
]