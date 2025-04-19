from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import apenas_admin, apenas_staff
from django.contrib import messages
from hotel.forms import ReservaForm
from hotel.models import Hotel, Quarto, Reserva
from django.http import JsonResponse
from hotel.tasks import enviar_email_confirmacao

from django.http import HttpResponse

def cadastro(request):
    if request.method == 'GET':
        return(render(request, 'cadastro.html'))
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if not username or not email or not senha:
            return render(request, 'cadastro.html', {'erro': 'Preencha todos os campos!'})

        mail = User.objects.filter(email = email).first()
        if mail:
            return render(request, 'cadastro.html', {'erro': 'você ja possui uma conta vinculada a este email'})
        
        user = User.objects.filter(username = username).first()
        if user:
            return render(request, 'cadastro.html', {'erro': 'este nome de usuario ja esta sendo utilizado'})
    
        user = User.objects.create_user(username, email, senha)
        user.save()    
        return render(request, 'login.html', {'erro': 'cadastro realizado com sucesso'})


def recebe_login(request):
    if request.method == 'GET':
        return(render(request, 'login.html'))
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            tipo = user.perfil.tipo

            # Redirecionando com base no tipo de usuário
            if tipo == 'admin':
                return redirect('painel_admin')  #URL para admin
            elif tipo == 'staff':
                return redirect('painel_staff')  #URL para staff
            else:
                return redirect('painel_cliente')  #URL para cliente
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'}) 


@login_required(login_url="/login/")
def painel_cliente(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.save()
            messages.success(request, 'Reserva realizada com sucesso!')

            nome_usuario = request.user.username
            email_cliente = request.user.email
            hotel = reserva.hotel.nome
            quarto = reserva.quarto.numero
            checkin = reserva.data_checkin.strftime('%d/%m/%Y')
            checkout = reserva.data_checkout.strftime('%d/%m/%Y')
            
            #messages.success(request, email_cliente)
            enviar_email_confirmacao.delay(nome_usuario,hotel,quarto,checkin,checkout,email_cliente,)

            return redirect('painel_cliente')

    else:
        form = ReservaForm()

    reservas = Reserva.objects.filter(cliente=request.user)
    return render(request, 'painel_cliente.html', {'form': form, 'reservas': reservas})


@login_required(login_url="/login/")
@apenas_staff
def painel_staff(request):
    hoteis = Hotel.objects.all()
    return render(request, 'painel_staff.html', {'hoteis': hoteis})


@login_required(login_url="/login/")
@apenas_admin
def painel_admin(request):
    if request.method == 'POST':

        user_id = request.POST.get('user_id')
        novo_tipo = request.POST.get('tipo')

        user = User.objects.get(id=user_id)
        user.perfil.tipo = novo_tipo
        user.perfil.save()

        return redirect('painel_admin')
    
    usuarios = User.objects.exclude(id=request.user.id)  # não mostra o próprio admin
    hoteis = Hotel.objects.all()
    return render(request, 'painel_admin.html', {
        'usuarios': usuarios,
        'hoteis' : hoteis, 
    })


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.perfil.tipo == 'admin')
def excluir_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    #Evita que o admin exclua a si mesmo (segurança redundante)
    if request.user == user:
        return redirect('painel_admin') 
    
     # Evita excluir outros admins
    if hasattr(user, 'perfil') and user.perfil.tipo == 'admin':
        messages.error(request, 'Você não pode excluir um administrador!')
        return redirect('painel_admin')

    user.delete()
    return redirect('painel_admin')


def sair(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/login/")
def carregar_quartos(request):
    hotel_id = request.GET.get('hotel')
    quartos = Quarto.objects.filter(hotel_id=hotel_id).values('id', 'numero')
    return JsonResponse(list(quartos), safe=False)


