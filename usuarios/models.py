from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = [
        ('cliente', 'Cliente'),
        ('staff', 'Staff'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='cliente')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"
