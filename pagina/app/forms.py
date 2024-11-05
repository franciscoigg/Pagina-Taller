from django import forms
from app.models import Tatuador, Cliente, Cita
from django.contrib.auth.models import User



class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class TatuadorForm(forms.ModelForm):
    class Meta:
        model = Tatuador
        fields = ['nombre', 'especialidad', 'disponibilidad', 'telefono','email']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['tatuador', 'fecha', 'hora']
        widgets={
            'fecha':forms.DateInput(attrs={'type':'date'}),
            'hora':forms.TimeInput(attrs={'type':'time'}),
        }

class AgregarCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['tatuador','cliente','fecha', 'hora']
        widgets={
            'fecha':forms.DateInput(attrs={'type':'date'}),
            'hora':forms.TimeInput(attrs={'type':'time'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("¡Las contraseñas no coinciden!")

        return cleaned_data


