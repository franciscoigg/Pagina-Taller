from django import forms
from app.models import Tatuador, Cliente, Usuario, Cita, Notificacion

class TatuadorForm(forms.ModelForm):
    class Meta:
        model = Tatuador
        fields = ['nombre', 'especialidad', 'disponibilidad', 'telefono']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usuario', 'contrasena', 'cliente']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'estado', 'tatuador', 'cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['mensaje', 'tatuador', 'usuario', 'cita']