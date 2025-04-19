from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import apenas_admin
from .models import Quarto, Hotel, Reserva
from django.contrib import messages
from .forms import HotelForm
from django.http import JsonResponse
from datetime import datetime


@login_required(login_url="/login/")
@apenas_admin
def cadastrar_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save()
            num_quartos = form.cleaned_data['numero_quartos']

            for i in range(1, num_quartos + 1):
                Quarto.objects.create(hotel=hotel, numero=str(i))

            messages.success(request, f'Hotel "{hotel.nome}" com {num_quartos} quartos criado com sucesso!')
            return redirect('cadastrar_hotel')
    else:
        form = HotelForm()
    return render(request, 'cadastrar_hotel.html', {'form': form})


@login_required(login_url="/login/")
@apenas_admin
def editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            hotel = form.save()

            num_quartos_atual = hotel.quarto_set.count()
            novo_total = hotel.numero_quartos

            if novo_total > num_quartos_atual: #Adiciona quartos a mais caso necessario
                for i in range(num_quartos_atual + 1, novo_total + 1):
                    Quarto.objects.create(hotel=hotel, numero=i)
            
            elif novo_total < num_quartos_atual: #Exclui os quartos com número maior que o novo total
                hotel.quarto_set.filter(numero__gt=novo_total).delete()

            return redirect('painel_admin')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'editar_hotel.html', {'form': form})


@login_required(login_url="/login/")
@apenas_admin
def excluir_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        hotel.delete()
        return redirect('painel_admin')

    return render(request, 'excluir_hotel.html', {'hotel': hotel})


@login_required(login_url="/login/")
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)
    reserva.delete()
    messages.success(request, "Reserva cancelada com sucesso.")
    return redirect('painel_cliente')

def verificar_quartos(request):
    hotel_id = request.GET.get('hotel_id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if not hotel_id or not checkin or not checkout:
        hotel_id = request.GET.get('hotel_id')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')

    try:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'erro': 'Datas inválidas'}, status=400)
    
    if checkin_date >= checkout_date:
        return JsonResponse({'erro': 'Checkout deve ser após check-in'}, status=400)

    # Todos os quartos do hotel
    quartos = Quarto.objects.filter(hotel_id=hotel_id)
    resultado = []

    for quarto in quartos:
        ocupado = Reserva.objects.filter(
            quarto=quarto,
            data_checkin__lte=checkout_date,
            data_checkout__gt=checkin_date
        ).exists()

        resultado.append({
            'numero': quarto.numero,
            'ocupado': ocupado
        })

    return JsonResponse({'quartos': resultado})
