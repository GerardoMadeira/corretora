from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import ClienteForm
from .models import Cliente


class ClienteListView(LoginRequiredMixin, ListView):
    """[READ - GERAL] - Lista os clientes do corretor logado e aceita buscas"""

    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"

    def get_queryset(self):
        # 1. Garante que só puxe os clientes pertencentes ao corretor logado
        queryset = Cliente.objects.filter(usuario=self.request.user)

        # 2. Captura o termo de busca enviado pela URL (ex: ?q=gerardo)
        busca = self.request.GET.get("q")

        # 3. Se o corretor digitou algo, filtra por Nome OU Documento OU E-mail
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca)
                | Q(documento__icontains=busca)
                | Q(email__icontains=busca)
            )

        return queryset


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """[READ - ESPECÍFICO] - Ficha cadastral detalhada de um único cliente"""

    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """[CREATE] - Cadastro de novos clientes"""

    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """[UPDATE] - Edição de dados do cliente"""

    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"  # Reutiliza o mesmo HTML do cadastro
    success_url = reverse_lazy("clientes:listar")

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """[DELETE] - Exclusão do cliente do sistema"""

    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("clientes:listar")

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)
