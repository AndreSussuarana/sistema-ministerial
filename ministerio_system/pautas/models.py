from typing import Any

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PerfilUsuario(models.Model):
    """Representa os papéis específicos dos usuários no sistema."""

    class ListaDeCargo(models.TextChoices):
        SECRETARIA = "SECRETARIA", "Secretaria(o)"
        LIDER = "LIDER", "Líder de Setor"
        ADMIN = "PASTOR", "Pastor / Dirigente"
    class Meta: 
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20, choices=ListaDeCargo.choices, default=ListaDeCargo.LIDER)
    departamento = models.CharField(max_length=150, blank=True, null=True)
    telefone_contato = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_cargo_display()})"# type: ignore
    
    def is_secretaria(self) -> bool:
        return self.cargo == self.ListaDeCargo.SECRETARIA.value

    def is_lider(self):
        return self.cargo == self.ListaDeCargo.LIDER.value
    
class Pauta(models.Model):
    """Representa uma pauta/tópico submetido para discussão."""

    class StatusPauta(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADA = "APROVADA", "Aprovada para Reunião"
        REPROVADA = "REPROVADA", "Reprovada"
        ADIADA = "ADIADA", "Adiada"
        APENAS_INFORMATIVA = "APENAS INFORMATIVA", "Apenas Informativa"
        
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(
        help_text="Descrição detalhada ou justificativa do assunto."
    )
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pautas_enviadas"
    )
    departamento = models.CharField(max_length=150, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=StatusPauta.choices, default=StatusPauta.PENDENTE
    )
    anexo = models.FileField(upload_to="pautas_anexos/", blank=True, null=True)
    resolucao = models.TextField(blank=True, null=True, verbose_name="Texto da Deliberação")
    situacao = models.CharField(max_length=20, choices=StatusPauta.choices, default=StatusPauta.PENDENTE)
    
    class Meta:
        verbose_name = "Pauta"
        verbose_name_plural = "Pautas"

    def __str__(self) -> str:
        return self.titulo

class Reuniao(models.Model):
    """Representa a Reunião/Sessão oficial do ministério."""
    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"
        ordering = ('-data_hora',)

    class StatusReuniao(models.TextChoices):
        AGENDADA = "AGENDADA", "Agendada"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em Andamento"
        CONCLUIDA = "CONCLUIDA", "Concluida"
        CANCELADA = "CANCELADA", "Cancelada"

    titulo = models.CharField(max_length=200, verbose_name="Título da Reunião")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    local = models.CharField(max_length=255, verbose_name="Local", default="Igreja Sede")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição / Observações")
    status = models.CharField(max_length=20, choices=StatusReuniao.choices, default=StatusReuniao.AGENDADA)
    presidida_por = models.CharField(max_length=150, blank=True, null=True)
    devocional_anotacoes = models.TextField(blank=True, null=True, verbose_name="Abertura e Devocional")
    observacoes_finais = models.TextField(blank=True, null=True)
    horario_termino = models.TimeField(blank=True, null=True)

    prazo_limite_pautas = models.DateTimeField(
        blank=True, null=True
    )

    pautas = models.ManyToManyField( # type: ignore
        Pauta, related_name="reunioes", blank=True, verbose_name="Pautas Vinculadas"
    ) 
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    def __str__(self) -> str:
        return f"{self.titulo} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def clean(self) -> None:
        super().clean()
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError({
                "data_hora": (
                    "Atenção: Não é permitido agendar uma sessão para uma data no passado!"
                )
            })
        if self.data_hora and self.local:
            existe_duplicada: bool = (
                Reuniao.objects.filter(data_hora=self.data_hora, local=self.local)
                .exclude(pk=self.pk)
                .exists()
            )
            if existe_duplicada:
                raise ValidationError({
                    "data_hora": "Já existe outra sessão agendada para este local neste mesmo horário!"
                })
                
    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError(
                "Não é permitido apagar sessões que já ocorreram no passado!"
            )
        return super().delete(*args, **kwargs)
    
class Presenca(models.Model):
    """Classe para listagem da presença"""
    class StatusPresenca(models.TextChoices):
        VOU = "VOU", "Vou"
        NAO_VOU = "NAO_VOU", "Não Vou"

    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='presencas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusPresenca.choices, default="VOU")

    class Meta:
        unique_together = ("reuniao", "usuario")

    def __str__(self) -> str:
        return f"{self.usuario.username} - {self.get_status_display()} ({self.reuniao.titulo})"