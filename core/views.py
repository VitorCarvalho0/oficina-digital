import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Atendimento, FotoAtendimento

# Função auxiliar para o xhtml2pdf localizar arquivos estáticos e de mídia no disco
def link_callback(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        return uri
    return path


def criar_conta(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fazer_login')
    else:
        form = UserCreationForm()
    return render(request, 'core/cadastro.html', {'form': form})


def fazer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def dashboard(request):
    atendimentos = Atendimento.objects.filter(usuario=request.user).order_by('-data_criacao')
    total_em_atendimento = atendimentos.exclude(status='finalizado').count()
    total_finalizados = atendimentos.filter(status='finalizado').count()

    context = {
        'atendimentos': atendimentos,
        'total_em_atendimento': total_em_atendimento,
        'total_finalizados': total_finalizados,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def novo_atendimento(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        telefone = request.POST.get('telefone')
        veiculo = request.POST.get('veiculo')
        placa = request.POST.get('placa')
        letra_vidro = request.POST.get('letra_vidro')
        
        ano_str = request.POST.get('ano')
        km_str = request.POST.get('km')
        ano = int(ano_str) if ano_str else 0
        km = int(km_str) if km_str else 0
        
        observacoes = request.POST.get('observacoes')
        
        foto_frente = request.FILES.get('foto_frente')
        foto_tras = request.FILES.get('foto_tras')
        foto_lat_esq = request.FILES.get('foto_lat_esq')
        foto_lat_dir = request.FILES.get('foto_lat_dir')

        atendimento = Atendimento.objects.create(
            usuario=request.user,
            cliente=cliente,
            telefone=telefone,
            veiculo=veiculo,
            placa=placa,
            letra_vidro=letra_vidro,
            ano=ano,
            km=km,
            observacoes=observacoes,
            foto_frente=foto_frente,
            foto_tras=foto_tras,
            foto_lat_esq=foto_lat_esq,
            foto_lat_dir=foto_lat_dir
        )

        for key, arquivo in request.FILES.items():
            if key.startswith('foto_extra_'):
                identificador = key.split('_')[-1]
                titulo = request.POST.get(f'titulo_foto_foto_extra_{identificador}', 'Detalhe')
                
                FotoAtendimento.objects.create(
                    atendimento=atendimento,
                    titulo=titulo,
                    imagem=arquivo
                )

        return redirect('dashboard')

    return render(request, 'core/novo_atendimento.html')


@login_required
def detalhe_atendimento(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        atendimento.cliente = request.POST.get('cliente', atendimento.cliente)
        atendimento.telefone = request.POST.get('telefone', atendimento.telefone)
        atendimento.veiculo = request.POST.get('veiculo', atendimento.veiculo)
        atendimento.placa = request.POST.get('placa', atendimento.placa)
        atendimento.letra_vidro = request.POST.get('letra_vidro', atendimento.letra_vidro)
        
        ano_str = request.POST.get('ano')
        km_str = request.POST.get('km')
        if ano_str is not None:
            atendimento.ano = int(ano_str) if ano_str else 0
        if km_str is not None:
            atendimento.km = int(km_str) if km_str else 0
            
        atendimento.observacoes = request.POST.get('observacoes', atendimento.observacoes)
        atendimento.status = request.POST.get('status', atendimento.status)
        
        if request.FILES.get('foto_frente'):
            atendimento.foto_frente = request.FILES.get('foto_frente')
        if request.FILES.get('foto_tras'):
            atendimento.foto_tras = request.FILES.get('foto_tras')
        if request.FILES.get('foto_lat_esq'):
            atendimento.foto_lat_esq = request.FILES.get('foto_lat_esq')
        if request.FILES.get('foto_lat_dir'):
            atendimento.foto_lat_dir = request.FILES.get('foto_lat_dir')
            
        atendimento.save()
        return redirect('detalhe_atendimento', pk=atendimento.pk)

    return render(request, 'core/detalhe_atendimento.html', {'atendimento': atendimento})


# Página pública para o cliente acompanhar o status do veículo
def acompanhar_atendimento(request, token):
    atendimento = get_object_or_404(Atendimento, token=token)
    return render(request, 'core/acompanhar_atendimento.html', {'atendimento': atendimento})


# View para geração do relatório em PDF
@login_required
def gerar_pdf_atendimento(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk, usuario=request.user)
    template = get_template('core/pdf_atendimento.html')
    context = {'atendimento': atendimento}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Checklist_{atendimento.placa}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response
