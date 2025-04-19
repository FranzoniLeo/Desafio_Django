from celery import shared_task
from django.core.mail import send_mail
from datetime import date
from hotel.models import Reserva

@shared_task
def enviar_email_confirmacao(usuario,hotel,quarto,checkin,checkout,email_cliente):
    assunto = "Confirmação de Reserva"
    mensagem = (
        f"Prezado(a) Sr(a). {usuario}.\n" 
        f"Sua reserva no hotel: {hotel}, quarto: {quarto}, foi confirmada com sucesso!\n"
        f"Sua estadia vai de {checkin} até {checkout}"
    )
    send_mail(
        assunto,
        mensagem,
        'franzoni.leoalves@gmail.com',  # remetente
        [email_cliente],             # destinatário
        fail_silently=False,
    )

@shared_task
def excluir_reservas():
    hoje = date.today()
    reservas = Reserva.objects.filter(data_checkout=hoje)

    total = reservas.count()
    reservas.delete()

    return f"{total} reservas removidas com checkout em {hoje}"