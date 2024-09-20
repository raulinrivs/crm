from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from authentication.models import CustomUser, Funcao


class UserCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "cpf", "endereco")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "filial",
                    "funcoes"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "data_admissao", "data_senha")}),
    )
    filter_horizontal = ("funcoes",)
    list_filter = ("is_staff", "is_superuser", "is_active")
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')


class FuncaoCustomAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "permissions",
    )


# Register your models here.
admin.site.register(CustomUser, UserCustomAdmin)
admin.site.register(Funcao, FuncaoCustomAdmin)
admin.site.register(Permission)
