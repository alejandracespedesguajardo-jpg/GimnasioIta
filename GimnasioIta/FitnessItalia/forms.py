
import os
import re
from django import forms
from .models import Cliente, Servizio, Prenotazione


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email', 'foto']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip()
        rut_limpio = re.sub(r'[.\-\s]', '', rut).upper()

        coincidencia = re.fullmatch(r'(\d{1,8})([\dK])', rut_limpio)

        if not coincidencia:
            raise forms.ValidationError('Inserire un RUT cileno valido. Esempio: 12.345.678-9.')

        numero = coincidencia.group(1)
        dv_ingresado = coincidencia.group(2)

        suma = 0
        multiplicador = 2

        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)

        if resto == 11:
            dv_calculado = '0'
        elif resto == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(resto)

        if dv_ingresado != dv_calculado:
            raise forms.ValidationError('Il RUT inserito non è valido. Verificare il codice di controllo.')

        return f'{int(numero):,}'.replace(',', '.') + '-' + dv_ingresado

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        telefono = re.sub(r'[\s().-]', '', telefono)

        if re.fullmatch(r'9\d{8}', telefono):
            telefono = '+56' + telefono
        elif re.fullmatch(r'569\d{8}', telefono):
            telefono = '+' + telefono

        if not re.fullmatch(r'\+569\d{8}', telefono):
            raise forms.ValidationError('Il numero di cellulare deve essere cileno. Esempio: +56912345678.')

        return telefono

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            extension = os.path.splitext(foto.name)[1].lower()
            if extension not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('La foto deve essere un file JPG o PNG.')
        return foto


class ServizioForm(forms.ModelForm):
    class Meta:
        model = Servizio
        fields = ['nome', 'descrizione', 'istruttore', 'prezzo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disciplina'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'istruttore': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Istruttore'}),
            'prezzo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }


class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['servizio', 'fecha_clase', 'hora_clase']
        widgets = {
            'servizio': forms.Select(attrs={'class': 'form-select'}),
            'fecha_clase': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_clase': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
