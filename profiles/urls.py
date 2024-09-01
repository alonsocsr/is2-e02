from django.urls import path
from .views import UpdateProfile


urlpatterns = [
    path("profile/", UpdateProfile.as_view(), name='profile'),
]