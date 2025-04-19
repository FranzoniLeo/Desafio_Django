from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('login/', views.recebe_login, name='login'),
    path('painel_cliente/', views.painel_cliente, name='painel_cliente'),
    path('painel_staff/', views.painel_staff, name='painel_staff'),
    path('painel_adimin/', views.painel_admin, name='painel_admin'),
    path('excluir-usuario/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('logout/', views.sair, name='logout'),
    path('ajax/carregar-quartos/', views.carregar_quartos, name='carregar_quartos'),
]

