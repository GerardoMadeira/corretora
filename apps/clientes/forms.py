from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Esconde o usuário logado, a data de cadastro e o antigo booleano ativo
        exclude = ["usuario", "data_cadastro", "ativo"]

        widgets = {
            # Tipo de Cliente (PF/PJ) - Puxa as choices da Model com design arredondado
            "tipo": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
            # Novo Status do CRM - Essencial para a esteira de evolução do cliente
            "status": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
            # Identificação e Contato
            "nome": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Nome completo ou razão social",
                }
            ),
            "documento": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "CPF ou CNPJ",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "email@exemplo.com",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "(11) 99999-9999",
                }
            ),
            "data_nascimento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
            # Bloco de Endereço Completo
            "cep": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "00000-000",
                }
            ),
            "logradouro": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Rua, Avenida, etc.",
                }
            ),
            "numero": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "123",
                }
            ),
            "complemento": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Apto, Bloco, Casa (Opcional)",
                }
            ),
            "bairro": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
            "cidade": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
            # Estado (UF) - Alterado para Select para carregar a lista ESTADOS_BR blindada da Model
            "estado": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500",
                }
            ),
        }
