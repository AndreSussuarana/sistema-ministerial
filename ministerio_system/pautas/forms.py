from typing import Any, ClassVar

from django import forms

from .models import Pauta, Reuniao


class PautaForm(forms.ModelForm): # type:ignore

    class Meta: 
        model = Pauta
        fields = ("titulo", "descricao", "departamento", "anexo")
        widgets: ClassVar[dict[str, Any]] = { 
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Compra de novos hinários",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                    "Descreva os detalhes e a justificativa do assunto..."
                    ),
                }
            ),
            "departamento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Ministério da Música",
                }
            ),
            "anexo": forms.FileInput(attrs={"class": "form-control"}),
        }
class ReuniaoForm(forms.ModelForm): # type: ignore
    class Meta:
        model = Reuniao
        fields = ("titulo", "data_hora", "local", "descricao", "prazo_limite_pautas", "pautas")
        widgets: ClassVar[dict[str, Any]] = {
            "titulo": forms.TextInput(
                attrs={"class":"form-control",
                       "placeholder": "Ex: Reunião Ministerial rotineira"}
            ),
            "data_hora": forms.DateTimeInput(
                attrs={"class": "form-control",
                       "type": "datetime-local"}
            ),
            "local": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Templo Sede"}
            ),
            "descricao": forms.Textarea(
                attrs={"class": "form-control",
                       "rows": 5,
                       "placeholder": "Notas gerais da futura reunião"}
            ),
            "prazo_limites_pautas": forms.DateTimeInput(
                attrs={"class": "form-control",
                       "type": "datetime-local"}
            ),
            "pautas": forms.SelectMultiple(
                attrs={"class": "form-control",
                       "size": "6"}
            )
        }