from typing import cast

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PautaForm, ReuniaoForm, UserRegisterForm
from .models import Pauta, Reuniao


def listar_pautas(request: HttpRequest) -> HttpResponse:
    """Lista as pautas (acesso público)."""
    pautas = Pauta.objects.all().order_by("-data_criacao")
    return render(request, "pautas/listar_pautas.html", {"pautas": pautas})

def criar_pauta(request: HttpRequest) -> HttpResponse:
    """Permite submeter uma nova pauta (acesso público)."""
    if request.method == "POST":
        form = PautaForm(request.POST, request.FILES)
        if form.is_valid():
            pauta = cast(Pauta, form.save(commit=False))
            if request.user.is_authenticated:
                pauta.autor = request.user # type: ignore
            pauta.save()
            return redirect("pautas:listar_pautas")
    else:
        form = PautaForm()
    return render(request, "pautas/criar_pauta.html", {"form": form})

def listar_reunioes(file_request: HttpRequest) -> HttpResponse:
    """Lista todas as reuniões agendadas ou realizadas (acesso público)"""
    reunioes = Reuniao.objects.all()
    return render(file_request, "pautas/listar_reunioes.html", {"reunioes": reunioes})

def criar_reuniao(request: HttpRequest) -> HttpResponse:
    """Permite agendar uma nova reunião (acesso público)."""
    if request.method == "POST":
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pautas:listar_reunioes")
    else:
        form = ReuniaoForm()
    return render(request, "pautas/criar_reuniao.html", {"form": form})

def editar_pauta(request: HttpRequest, pk: int) -> HttpResponse:
    pauta = get_object_or_404(Pauta, pk=pk)
    if request.method == "POST":
        form = PautaForm(request.POST, instance=pauta)
        if form.is_valid():
            form.save()
            return redirect('pautas:listar_pautas')
    else:
        form = PautaForm(instance=pauta)
    return render(request, 'pautas/editar_pauta.html', {'form': form, 'pauta': pauta})

def editar_reuniao(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
            return redirect('pautas:listar_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)
    return render(request, 'pautas/editar_reuniao.html', {'form': form, 'reuniao': reuniao})

def detalhe_reuniao(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    pautas_reuniao = reuniao.pautas.all() # type: ignore
    
    return render(request, 'pautas/detalhe_reuniao.html', {
        'reuniao': reuniao,
        'pautas_reuniao': pautas_reuniao
    })

def modo_reuniao(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    pautas = reuniao.pautas.all() # type:ignore
    
    if request.method == "POST":
        reuniao.presidida_por = request.POST.get('presidida_por')
        reuniao.devocional_anotacoes = request.POST.get('devocional_anotacoes')
        reuniao.observacoes_finais = request.POST.get('observacoes_finais')
        reuniao.save()
        
        for pauta in pautas: # type:ignore
            resolucao_texto = request.POST.get(f'resolucao_{pauta.pk}') # type:ignore
            situacao_status = request.POST.get(f'situacao_{pauta.pk}')  # type:ignore
            if resolucao_texto is not None:
                pauta.resolucao = resolucao_texto
                pauta.situacao = situacao_status
                pauta.save()  # type:ignore
                
        return redirect('pautas:modo_reuniao', pk=reuniao.pk)

    return render(request, 'pautas/modo_reuniao.html', {
        'reuniao': reuniao,
        'pautas': pautas
    })

def gerar_ata(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    pautas = reuniao.pautas.all() # type:ignore
    presencas = reuniao.presencas.all() # type:ignore
    
    return render(request, 'pautas/ata_reuniao.html', {
        'reuniao': reuniao,
        'pautas': pautas,
        'presencas': presencas
    })

def concluir_reuniao(request: HttpRequest, pk: int):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    reuniao.status = Reuniao.StatusReuniao.CONCLUIDA
    reuniao.save()
    
    messages.success(request, f"A reunião '{reuniao.titulo}' foi concluída com sucesso e a ata foi fechada!")
    return redirect('pautas:detalhe_reuniao', pk=reuniao.pk)

def detalhe_pauta(request: HttpRequest, pk: int) -> HttpResponse:
    pauta = get_object_or_404(Pauta, pk=pk)
    return render(request, 'pautas/detalhe_pauta.html', {'pauta': pauta})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Já podes fazer login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'pautas/register.html', {'form': form})

def dashboard(request: HttpRequest) -> HttpResponse:
    """Painel inicial aberto a todos."""
    proxima_reuniao = Reuniao.objects.exclude(status='CONCLUIDA').order_by('data_hora').first()

    context = { # type: ignore
        'proxima_reuniao': proxima_reuniao,
        'is_secretaria_or_admin': True  # Libera tudo visualmente também
    }
    return render(request, 'pautas/dashboard.html', context) # type: ignore

def criar_admin_emergencia(request: HttpRequest):
    if not User.objects.filter(username='chefe').exists():
        User.objects.create_superuser('chefe', 'chefe@email.com', 'senha12345')
        return HttpResponse("Sucesso! Superutilizador 'chefe' criado com a senha 'senha12345'.")
    return HttpResponse("O utilizador 'chefe' já existe!")