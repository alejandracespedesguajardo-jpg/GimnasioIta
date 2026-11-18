from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=16, unique=True, verbose_name="Codice Fiscale / Documento")
    nombre = models.CharField(max_length=50, verbose_name="Nome")
    apellido = models.CharField(max_length=50, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Indirizzo Email")
    telefono = models.CharField(max_length=15, verbose_name="Telefono")
    foto = models.ImageField(upload_to='clientes/', null=True, blank=True, verbose_name="Foto Profilo")
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

    def delete(self, using=None, keep_parents=False):
        if self.foto:
            self.foto.storage.delete(self.foto.name)
        super().delete()


class Servizio(models.Model):
    nome = models.CharField(max_length=60, verbose_name="Disciplina")
    descrizione = models.TextField(verbose_name="Descrizione")
    istruttore = models.CharField(max_length=60, verbose_name="Istruttore")
    prezzo = models.IntegerField(verbose_name="Prezzo Sessione (€)")

   

    def __str__(self):
        return f"{self.nome} - Prof. {self.istruttore}"

ESTADOS = [
    ('Confermata', 'Confermata'),
    ('Annullata', 'Annullata'),
]


class Prenotazione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    servizio = models.ForeignKey(Servizio, on_delete=models.CASCADE, verbose_name="Disciplina")
    fecha_clase = models.DateField(verbose_name="Data della Lezione")
    hora_clase = models.TimeField(verbose_name="Ora della Lezione")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Confermata', verbose_name="Stato")

    def __str__(self):
        return f"{self.cliente.nombre} - {self.servizio.nome}"

class Membresia(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Tipo di Abbonamento")
    duracion_meses = models.IntegerField(verbose_name="Durata (Mesi)")
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prezzo (€)")

    def __str__(self):
        return f"{self.nombre} - €{self.precio}"