from django.db import models
from django.contrib.auth.models import User

class Tatuador(models.Model):
    OPCIONES_DISPONIBILIDAD = [
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tatuador_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=True)
    especialidad = models.CharField(max_length=30, null=True)
    disponibilidad = models.CharField(max_length=20, choices=OPCIONES_DISPONIBILIDAD, default='Disponible')
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    email = models.EmailField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cliente_id = models.AutoField(primary_key=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    email = models.EmailField(max_length=30, null=True, unique=True)
    nombre = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.nombre

class EstadoCita(models.Model):
    estado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    cita_id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    estado = models.ForeignKey(EstadoCita, on_delete=models.SET_NULL, null=True)
    tatuador = models.ForeignKey(Tatuador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Cita con {self.tatuador.nombre} para {self.cliente.nombre} el {self.fecha} a las {self.hora}'