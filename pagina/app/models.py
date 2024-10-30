from django.db import models

class Tatuador(models.Model):
    tatuador_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=True)
    especialidad = models.CharField(max_length=30, null=True)
    disponibilidad = models.CharField(max_length=20, null=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True)

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    email = models.EmailField(max_length=30, null=True)
    nombre = models.CharField(max_length=40, null=True)

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=40, null=True)
    contrasena = models.CharField(max_length=20, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Cita(models.Model):
    cita_id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    hora = models.DateTimeField(null=True)
    estado = models.CharField(max_length=20, null=True)
    tatuador = models.ForeignKey(Tatuador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Notificacion(models.Model):
    notificacion_id = models.AutoField(primary_key=True)
    mensaje = models.CharField(max_length=80, null=True)
    tatuador = models.ForeignKey(Tatuador, null=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, null=True, on_delete=models.CASCADE)
