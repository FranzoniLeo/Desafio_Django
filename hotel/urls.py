from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_hotel/', views.cadastrar_hotel, name='cadastrar_hotel'),
    path('editar_hotel/<int:hotel_id>/', views.editar_hotel, name='editar_hotel'),
    path('excluir_hotel/<int:hotel_id>/', views.excluir_hotel, name='excluir_hotel'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('verificar-quartos/', views.verificar_quartos, name='verificar_quartos'),
]