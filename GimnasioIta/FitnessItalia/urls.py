from django.urls import path
from . import views

urlpatterns = [

    # publicaasss
    path('', views.lista_servizi, name='lista_servizi'),

    path('registrazione/', views.registrazione, name='registrazione'),

    # Protegidas con login
    path('inicio/', views.inicio, name='inicio'),

    path('prenota/', views.crea_prenotazione, name='crea_prenotazione'),

    path('mie-prenotazioni/', views.mie_prenotazioni, name='mie_prenotazioni'),

    path('annulla-prenotazione/<int:pk>/', views.annulla_prenotazione, name='annulla_prenotazione'),

    # Exclusivo del personal del Gym 
    path('clienti/', views.lista_clienti, name='lista_clienti'),

    path('clienti/nuovo/', views.crea_cliente, name='crea_cliente'),

    path('clienti/<int:pk>/modifica/', views.modifica_cliente, name='modifica_cliente'),

    path('clienti/<int:pk>/elimina/', views.elimina_cliente, name='elimina_cliente'),

    path('servizi/nuovo/', views.crea_servizio, name='crea_servizio'),

    path('servizi/<int:pk>/modifica/', views.modifica_servizio, name='modifica_servizio'),

    path('servizi/<int:pk>/elimina/', views.elimina_servizio, name='elimina_servizio'),

    path('prenotazioni/', views.lista_prenotazioni, name='lista_prenotazioni'),

    path('abbonamenti/', views.lista_membresie, name='lista_membresie'),

]
