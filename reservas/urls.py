from django.urls import path
from .views import (CasaListAPIView, CasaDetailAPIView, CasaCreateAPIView, CasaUpdateAPIView, CasaDestroyAPIView,
                    AluguelCreateAPIView, AluguelListAPIView, AluguelUpdateAPIView, AluguelDestroyAPIView
                    )


urlpatterns = [
    path("casas/listar/", CasaListAPIView.as_view(), name="listar_casas"),
    path("casas/criar/", CasaCreateAPIView.as_view(), name="cadastrar_casas"),
    path("casas/<int:pk>/detalhes/", CasaDetailAPIView.as_view(), name="detalhar_casa"),
    path("casas/<int:pk>/editar/", CasaUpdateAPIView.as_view(), name="editar_casas"),
    path("casas/<int:pk>/excluir/", CasaDestroyAPIView.as_view(), name="excluir_casas"),

    path("aluguel/listar/", AluguelListAPIView.as_view(), name="listar_aluguel"),
    path("aluguel/<int:pk>/detalhe/", AluguelListAPIView.as_view(), name="detalhar_aluguel"),
    path("aluguel/<int:pk>/editar/", AluguelUpdateAPIView.as_view(), name="editar_aluguel"),
    path("aluguel/<int:pk>/excluir/", AluguelDestroyAPIView.as_view(), name="excluir_aluguel"),
    path("aluguel/criar/", AluguelCreateAPIView.as_view(), name="criar_aluguel")

]