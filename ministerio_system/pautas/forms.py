from typing import Any, ClassVar

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser

from .models import Pauta, Reuniao

User = get_user_model()
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
class UserRegisterForm(UserCreationForm): # type:ignore
    email = forms.EmailField(required=True, label="Endereço de e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar senha")

    class Meta: # type: ignore
        model = User # type:ignore
        fields = ['username', 'email'] # type:ignore  # noqa: RUF012

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As palavras-passe não coincidem.")
        return cleaned_data

    def save(self, commit: bool = True) -> AbstractBaseUser: # type:ignore
        user = super().save(commit=False) # type: ignore
        if isinstance(user, AbstractBaseUser):
            if commit:
                user.save()
            return user
        raise TypeError("O objeto retornado não é um utilizador válido.")