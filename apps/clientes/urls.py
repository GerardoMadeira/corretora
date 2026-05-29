from django.urls import path

from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteDetailView,  # Inclua ela aqui
    ClienteUpdateView,
    ClienteDeleteView,
)

app_name = "clientes"

urlpatterns = [
    path("", ClienteListView.as_view(), name="listar"),
    path("novo/", ClienteCreateView.as_view(), name="criar"),
    path(
        "<int:pk>/", ClienteDetailView.as_view(), name="detalhar"
    ),  # <--- Rota da Ficha do Cliente
    path("<int:pk>/editar/", ClienteUpdateView.as_view(), name="editar"),
    path("<int:pk>/excluir/", ClienteDeleteView.as_view(), name="excluir"),
]
