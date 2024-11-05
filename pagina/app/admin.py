from django.contrib import admin
from .models import Tatuador,Cita,Cliente,EstadoCita
# Register your models here.
 
class Tatuadoradmin(admin.ModelAdmin):
    list_display=("nombre","especialidad","disponibilidad","telefono")

class Citaadmin(admin.ModelAdmin):
    list_display=("fecha","hora","estado")

admin.site.register(Tatuador,Tatuadoradmin)

admin.site.register(Cita,Citaadmin)

admin.site.register(EstadoCita)

admin.site.register(Cliente)
