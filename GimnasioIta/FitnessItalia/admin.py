from django.contrib import admin
from .models import Cliente, Servizio, Prenotazione, Membresia


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('rut', 'nombre', 'apellido')


@admin.register(Servizio)
class ServizioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'istruttore', 'prezzo')
    search_fields = ('nome', 'istruttore')


@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servizio', 'fecha_clase', 'hora_clase', 'estado')
    list_filter = ('estado', 'fecha_clase')
    search_fields = ('cliente__nombre', 'cliente__apellido')


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_meses', 'precio')
