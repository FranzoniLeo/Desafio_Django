from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    nome = models.CharField(max_length=100)
    numero_quartos = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class Quarto(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f'Quarto {self.numero} - {self.hotel.nome}'


class Reserva(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    data_checkin = models.DateField()
    data_checkout = models.DateField()

    def __str__(self):
        return f'Reserva de {self.cliente.username} - {self.quarto}'
    


