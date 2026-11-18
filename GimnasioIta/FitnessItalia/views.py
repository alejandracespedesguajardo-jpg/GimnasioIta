from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Cliente, Servizio, Prenotazione, Membresia
from .forms import ClienteForm, ServizioForm, PrenotazioneForm

TESTO_PERSONALE = 'Questa pagina è riservata al personale della palestra.'
TESTO_CLIENTI = 'Solo i clienti registrati possono usare questa funzione.'


#estas son las públicas 
def lista_servizi(request):
    servizi = Servizio.objects.all()
    return render(request, 'FitnessItalia/lista_servizi.html', {'servizi': servizi})


def registrazione(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        cliente_form = ClienteForm(request.POST, request.FILES)
        if user_form.is_valid() and cliente_form.is_valid():
            utente = user_form.save()
            cliente = cliente_form.save()
            cliente.user = utente
            cliente.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
        cliente_form = ClienteForm()
    return render(request, 'FitnessItalia/registrazione.html',
                  {'user_form': user_form, 'cliente_form': cliente_form})


#página protegida 
@login_required
def inicio(request):
    return render(request, 'FitnessItalia/inicio.html')



#el cliente reserva al instructor 
@login_required
#el cliente reserva al instructor 
@login_required
def crea_prenotazione(request):
    cliente = Cliente.objects.filter(user=request.user).first()
    if cliente is None:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_CLIENTI})

    errore = ''
    if request.method == 'POST':
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            servizio = form.cleaned_data['servizio']
            data = form.cleaned_data['fecha_clase']
            ora = form.cleaned_data['hora_clase']
            if data < date.today():
                errore = 'La data non può essere nel passato.'
            elif ora.minute != 0 or ora.hour < 8 or ora.hour > 20:
                errore = 'Scegli un\'ora esatta tra le 08:00 e le 20:00.'
            elif Prenotazione.objects.filter(servizio=servizio, fecha_clase=data,
                                             hora_clase=ora, estado='Confermata').exists():
                errore = 'Questa lezione è già prenotata a quell\'ora.'
            elif Prenotazione.objects.filter(cliente=cliente, fecha_clase=data,
                                             hora_clase=ora, estado='Confermata').exists():
                errore = 'Hai già una prenotazione a quell\'ora.'
            else:
                Prenotazione.objects.create(cliente=cliente, servizio=servizio,
                                            fecha_clase=data, hora_clase=ora)
                return redirect('mie_prenotazioni')
    else:
        form = PrenotazioneForm()
    return render(request, 'FitnessItalia/form_prenotazione.html', {'form': form, 'errore': errore})


@login_required
def mie_prenotazioni(request):
    cliente = Cliente.objects.filter(user=request.user).first()
    if cliente is None:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_CLIENTI})
    prenotazioni = Prenotazione.objects.filter(cliente=cliente).order_by('-fecha_clase', '-hora_clase')
    return render(request, 'FitnessItalia/mie_prenotazioni.html', {'prenotazioni': prenotazioni})


@login_required
def annulla_prenotazione(request, pk):
    cliente = Cliente.objects.filter(user=request.user).first()
    if cliente is None:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_CLIENTI})
    # Solo se pueden anular las reservas propias
    prenotazione = get_object_or_404(Prenotazione, pk=pk, cliente=cliente)
    if request.method == 'POST':
        prenotazione.estado = 'Annullata'
        prenotazione.save()
    return redirect('mie_prenotazioni')


#Equipo del Gym en 2de puede realizar cambios CRUD
@login_required
def lista_clienti(request):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    clienti = Cliente.objects.all()
    return render(request, 'FitnessItalia/lista_clienti.html', {'clienti': clienti})


@login_required
def crea_cliente(request):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_clienti')
    else:
        form = ClienteForm()
    return render(request, 'FitnessItalia/form_cliente.html', {'form': form})


@login_required
def modifica_cliente(request, pk):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clienti')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'FitnessItalia/form_cliente.html', {'form': form, 'cliente': cliente})


@login_required
def elimina_cliente(request, pk):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        utente = cliente.user
        cliente.delete()
        if utente:
            utente.delete()
        return redirect('lista_clienti')
    return render(request, 'FitnessItalia/elimina_cliente.html', {'cliente': cliente})


@login_required
def crea_servizio(request):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    if request.method == 'POST':
        form = ServizioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servizi')
    else:
        form = ServizioForm()
    return render(request, 'FitnessItalia/form_servizio.html', {'form': form})


@login_required
def modifica_servizio(request, pk):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    servizio = get_object_or_404(Servizio, pk=pk)
    if request.method == 'POST':
        form = ServizioForm(request.POST, instance=servizio)
        if form.is_valid():
            form.save()
            return redirect('lista_servizi')
    else:
        form = ServizioForm(instance=servizio)
    return render(request, 'FitnessItalia/form_servizio.html', {'form': form, 'servizio': servizio})


@login_required
def elimina_servizio(request, pk):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    servizio = get_object_or_404(Servizio, pk=pk)
    if request.method == 'POST':
        servizio.delete()
        return redirect('lista_servizi')
    return render(request, 'FitnessItalia/elimina_servizio.html', {'servizio': servizio})


@login_required
def lista_prenotazioni(request):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    prenotazioni = Prenotazione.objects.all()
    return render(request, 'FitnessItalia/lista_prenotazioni.html', {'prenotazioni': prenotazioni})


@login_required
def lista_membresie(request):
    if not request.user.is_staff:
        return render(request, 'FitnessItalia/accesso_negato.html', {'testo': TESTO_PERSONALE})
    membresie = Membresia.objects.all()
    return render(request, 'FitnessItalia/lista_membresie.html', {'membresie': membresie})
