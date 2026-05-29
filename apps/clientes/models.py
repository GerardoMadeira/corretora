import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Lista oficial de Estados do Brasil para blindagem de dados
ESTADOS_BR = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]


class Cliente(models.Model):
    """
    Representa os clientes no sistema com esteira de CRM integrada.
    Cada cliente é indexado e vinculado exclusivamente a um corretor (User).
    """

    TIPO_CLIENTE_CHOICES = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]

    # Nova esteira de CRM profissional para Corretoras de Seguros
    STATUS_CRM_CHOICES = [
        ("LEAD", "Lead (Prospecção)"),
        ("COTACAO", "Em Cotação"),
        ("ATIVO", "Ativo (Com Apólice)"),
        ("INATIVO", "Inativo (Sem Apólice)"),
        ("CANCELADO", "Cancelado"),
    ]

    # Relacionamentos
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clientes",
        verbose_name="Corretor/Usuário",
    )

    # Identificação
    tipo = models.CharField(
        max_length=2,
        choices=TIPO_CLIENTE_CHOICES,
        default="PF",
        verbose_name="Tipo de Cliente",
    )
    nome = models.CharField(max_length=255, verbose_name="Nome / Razão Social")
    documento = models.CharField(max_length=14, verbose_name="CPF / CNPJ")
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name="Data de Nascimento"
    )

    # Campo de Evolução de CRM integrado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CRM_CHOICES,
        default="LEAD",
        verbose_name="Status no CRM",
    )

    # Contato
    email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name="E-mail"
    )
    telefone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Telefone/WhatsApp"
    )

    # Endereço
    cep = models.CharField(max_length=8, verbose_name="CEP")
    logradouro = models.CharField(max_length=255, verbose_name="Endereço/Rua")
    numero = models.CharField(max_length=20, verbose_name="Número")
    complemento = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Complemento"
    )
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2, choices=ESTADOS_BR, default="SP", verbose_name="UF"
    )

    # Auditoria
    data_cadastro = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Cadastro"
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

        # Adicionado o status no índice para acelerar filtros de relatórios do CRM
        indexes = [
            models.Index(fields=["nome"], name="cliente_nome_idx"),
            models.Index(fields=["email"], name="cliente_email_idx"),
            models.Index(fields=["status"], name="cliente_status_idx"),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "documento"], name="uniq_cliente_usuario_documento"
            )
        ]

    def __str__(self):
        return f"{self.nome} - {self.get_status_display()} ({self.documento})"

    def clean(self):
        """Valida e sanitiza os dados garantindo a integridade do CRM."""
        super().clean()

        # Padronizações de segurança
        if self.estado:
            self.estado = self.estado.strip().upper()
        if self.status:
            self.status = self.status.strip().upper()

        # Sanitização temporária dos campos numéricos para validação
        doc_limpo = re.sub(r"\D", "", self.documento) if self.documento else ""
        cep_limpo = re.sub(r"\D", "", self.cep) if self.cep else ""

        # Validações de comprimento do documento
        if self.tipo == "PF" and len(doc_limpo) != 11:
            raise ValidationError(
                {"documento": "CPF deve conter exatamente 11 dígitos."}
            )

        if self.tipo == "PJ" and len(doc_limpo) != 14:
            raise ValidationError(
                {"documento": "CNPJ deve conter exatamente 14 dígitos."}
            )

        # Persistência dos dados sanitizados
        self.documento = doc_limpo
        self.cep = cep_limpo

    def save(self, *args, **kwargs):
        """Camada de gravação segura."""
        self.full_clean()
        super(Cliente, self).save(*args, **kwargs)
