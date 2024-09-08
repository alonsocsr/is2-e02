from django.urls import path
from .views import UpdateProfile, categoria_interes



urlpatterns = [
    path("profile/", UpdateProfile.as_view(), name='profile'),
    path("misIntereses/<int:categoria_id>/", categoria_interes, name='categoria_interes')
]