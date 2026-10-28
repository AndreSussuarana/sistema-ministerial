from typing import cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PautaForm, ReuniaoForm, UserRegisterForm
from .models import Pauta, PerfilUsuario, Reuniao


@login_required
def listar_pautas(request: HttpRequest) -> HttpResponse:
    """Lista as pautas.

    Líderes veem apenas as suas; Secretária e Pastor veem todas.
    """

    perfil = PerfilUsuario.objects.filter(user=request.user).first()

    if perfil and (perfil.is_secretaria() or perfil.cargo == "PASTOR"):
        pautas = Pauta.objects.all().order_by("-data_criacao")
    else:
        pautas = Pauta.objects.filter(autor=request.user).order_by("-data_criacao")
    return render(request, "pautas/listar_pautas.html", {"pautas": pautas})

@login_required
def criar_pauta(request: HttpRequest) -> HttpResponse:
    """Permite submeter uma nova pauta."""
    if request.method == "POST":
        form = PautaForm(request.POST, request.FILES)
        if form.is_valid():
            pauta = cast(Pauta, form.save(commit=False))
            pauta.autor = request.user # type: ignore
            pauta.save()
            return redirect("pautas:listar_pautas")
    else:
        form = PautaForm()
    return render(request, "pautas/criar_pauta.html", {"form": form})

@login_required
def listar_reunioes(request: HttpRequest) -> HttpResponse:
    """Listaa todas as reuniões agendadas ou realizadas"""
    reunioes = Reuniao.objects.all()
    return render(request, "pautas/listar_reunioes.html", {"reunioes": reunioes})

@login_required
def criar_reuniao(request: HttpRequest) -> HttpResponse:
    """Permite agendar uma nova reunião."""
    if request.method == "POST":
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pautas:listar_reunioes")
    else:
        form = ReuniaoForm()
    return render(request, "pautas/criar_reuniao.html", {"form": form})

@login_required
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

@login_required
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

@login_required
def detalhe_reuniao(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    # Busca as pautas associadas a esta reunião (se houver relação ManyToMany ou ForeignKey)
    pautas_reuniao = reuniao.pautas.all() # type: ignore
    
    return render(request, 'pautas/detalhe_reuniao.html', {
        'reuniao': reuniao,
        'pautas_reuniao': pautas_reuniao
    })

@login_required
def modo_reuniao(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    pautas = reuniao.pautas.all() # type:ignore
    
    if request.method == "POST":
        # Atualiza dados gerais da reunião (anotações iniciais, presidência, etc.)
        reuniao.presidida_por = request.POST.get('presidida_por')
        reuniao.devocional_anotacoes = request.POST.get('devocional_anotacoes')
        reuniao.observacoes_finais = request.POST.get('observacoes_finais')
        reuniao.save()
        
        # Atualiza as resoluções de cada pauta enviada no formulário
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

@login_required
def gerar_ata(request: HttpRequest, pk: int) -> HttpResponse:
    reuniao = get_object_or_404(Reuniao, pk=pk)
    pautas = reuniao.pautas.all() # type:ignore
    presencas = reuniao.presencas.all() # type:ignore
    
    return render(request, 'pautas/ata_reuniao.html', {
        'reuniao': reuniao,
        'pautas': pautas,
        'presencas': presencas
    })

@login_required
def concluir_reuniao(request: HttpRequest, pk: int):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    

    perfil = getattr(request.user, 'perfilusuario', None)
    is_admin_or_sec = request.user.is_superuser or (perfil and perfil.is_secretaria())
    
    if not is_admin_or_sec:
        messages.error(request, "Não tens permissão para concluir reuniões.")
        return redirect('pautas:detalhe_reuniao', pk=reuniao.pk)

    reuniao.status = Reuniao.StatusReuniao.CONCLUIDA
    reuniao.save()
    
    messages.success(request, f"A reunião '{reuniao.titulo}' foi concluída com sucesso e a ata foi fechada!")
    return redirect('pautas:detalhe_reuniao', pk=reuniao.pk)

@login_required
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

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Painel inicial que destaca a próxima reunião e atalhos rápidos."""
    proxima_reuniao = Reuniao.objects.exclude(status='CONCLUIDA').order_by('data_hora').first()

    perfil = PerfilUsuario.objects.filter(user=request.user).first()
    is_secretaria_or_admin = request.user.is_superuser or (perfil and perfil.is_secretaria())

    context = { # type: ignore
        'proxima_reuniao': proxima_reuniao,
        'is_secretaria_or_admin': is_secretaria_or_admin
    }
    return render(request, 'pautas/dashboard.html', context) # type: ignore