from .views import UserRegisterAPIView
from django.urls import path


urlpatterns = [
    path('registrar/', UserRegisterAPIView.as_view(), name="registrar_user")
]