from django.urls import path
from .views import home_users,landing

urlpatterns = [
    path('home/', home_users, name='home'), 
    path('', landing, name='landing'),
]