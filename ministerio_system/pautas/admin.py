from typing import Any, ClassVar

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

from .models import Pauta, PerfilUsuario, Reuniao


class ReuniaoAdminForm(forms.ModelForm): # type:ignore
  class Meta:
    model = Reuniao
    fields = "__all__"
    widgets = {  # noqa: RUF012
        "data_hora": forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )
    }

  def clean(self) -> dict[str, Any]:
    cleaned_data = super().clean()
    try:
      instance: Reuniao = self.instance  # type: ignore[assignment]
      for field, value in cleaned_data.items():
        field_object = Reuniao._meta.get_field(field)
        if field_object.many_to_many:
          continue
        setattr(instance, field, value)  # type: ignore[arg-type]
      instance.clean() # type:ignore
    except ValidationError as e:
      if hasattr(e, "error_dict"):
        for field, error_list in e.error_dict.items():
          for error in error_list:
            self.add_error(field, error.message)
      else:
        raise
    return cleaned_data


class ReuniaoAdmin(admin.ModelAdmin): # type:ignore
  form = ReuniaoAdminForm
  # Força o admin a usar um DateTimeField simples em vez do SplitDateTimeField
  formfield_overrides: ClassVar = {  # type: ignore[assignment]
      models.DateTimeField: {
          "form_class": forms.DateTimeField,
          "widget": forms.DateTimeInput(
              attrs={"type": "datetime-local", "class": "form-control"}
          ),
      }
  }
  def has_add_permission(self, request: Any) -> bool:
    # Apenas superutilizadores ou membros com permissão podem adicionar sessões
    return request.user.is_superuser or request.user.is_staff

  def has_change_permission(self, request: Any, obj: Any | None = None) -> bool:
    return request.user.is_superuser or request.user.is_staff

  def has_delete_permission(self, request: Any, obj: Any | None = None) -> bool:
    # Restringe a exclusão apenas a superutilizadores por segurança
    return request.user.is_superuser

class PerfilUsuarioAdmin(admin.ModelAdmin): # type:ignore
  list_display = ("user", "cargo", "departamento", "telefone_contato")
  list_filter = ("cargo", "departamento")
  search_fields = ("user__username", "user__email", "departamento")

class PautaAdmin(admin.ModelAdmin): # type:ignore
  list_display = ("titulo", "autor", "departamento", "status", "data_criacao")
  list_filter = ("status", "departamento")
  search_fields = ("titulo", "descricao", "departamento")


# Registando os modelos no painel admin
admin.site.register(PerfilUsuario)
admin.site.register(Pauta)
admin.site.register(Reuniao, ReuniaoAdmin)