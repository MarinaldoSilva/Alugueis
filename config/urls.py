from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views #cuida dos tokens com funções nativas

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include('users.urls')),
    path("api/v1/reservas/", include('reservas.urls')),

    #criação de tokens do nosso novo usuario
    path("api/v1/auth/token/login/", views.obtain_auth_token, name='criar_token')
]
