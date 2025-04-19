from django import forms
from .models import Reserva, Hotel
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError


#criar um novo hotel
class HotelForm(forms.ModelForm):
    numero_quartos = forms.IntegerField(min_value=1, label='Número de Quartos')
    class Meta:
        model = Hotel
        fields = ['nome', 'numero_quartos']

#criar uma reserva de hotel
class ReservaForm(forms.ModelForm):

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=True)
    class Meta:
        model = Reserva
        fields = ['hotel', 'quarto', 'data_checkin', 'data_checkout']
        widgets = {
            'data_checkin': forms.DateInput(attrs={'type': 'date', 'min': now().date()}),
            'data_checkout': forms.DateInput(attrs={'type': 'date', 'min': now().date()}),
        }

    def clean_data_checkin(self):
        data_checkin = self.cleaned_data['data_checkin']
        if data_checkin < timezone.now().date():  #conferencia redundante
            raise forms.ValidationError("A data de check-in deve ser futura.") 
        return data_checkin

    def clean(self):
        cleaned_data = super().clean()
        quarto = cleaned_data.get('quarto')
        data_checkin = cleaned_data.get('data_checkin')
        data_checkout = cleaned_data.get('data_checkout')


        if quarto and data_checkin and data_checkout:
            conflitos = Reserva.objects.filter(
                quarto=quarto,
                data_checkin__lt=data_checkout,
                data_checkout__gt=data_checkin,
            )

            if data_checkout <= data_checkin:
                raise forms.ValidationError("A data de check-out deve ser posterior à de check-in.")
        
            if self.instance.pk:
                #Ignora a própria reserva (para casos de edição)
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                raise ValidationError("Este quarto já está reservado neste período.")
            
    

