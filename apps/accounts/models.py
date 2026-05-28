from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)

        extra_fields.setdefault("is_superuser", True)

        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email,
            password,
            **extra_fields,
        )


class User(AbstractUser):
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome",
    )

    nome_corretora = models.CharField(
        max_length=150,
        verbose_name="Nome da corretora",
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        unique=True,
    )

    username = None

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()
