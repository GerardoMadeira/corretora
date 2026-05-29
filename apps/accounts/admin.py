from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    ordering = ("email",)

    list_display = (
        "email",
        "nome",
        "nome_corretora",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "nome",
        "nome_corretora",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Informações",
            {
                "fields": (
                    "nome",
                    "nome_corretora",
                    "telefone",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Datas importantes",
            {"fields": ("last_login",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome",
                    "nome_corretora",
                    "telefone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
