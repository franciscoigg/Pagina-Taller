from django.shortcuts import render,redirect
from app.forms import TatuadorForm, ClienteForm, UsuarioForm, CitaForm, NotificacionForm

# Create your views here.

def index(request):
    return render(request,'app/index.html')

def tatuadores(request):
    return render(request,'app/tatuadores.html')

def agregar_tatuador(request):
    if request.method == 'POST':
        form = TatuadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio') 
    else:
        form = TatuadorForm()
    return render(request, 'app/agregar_tatuador.html', {'form': form})

# Define vistas similares para las otras tablas
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ClienteForm()
    return render(request, 'app/agregar_cliente.html', {'form': form})

def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = UsuarioForm()
    return render(request, 'app/agregar_usuario.html', {'form': form})

def agregar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = CitaForm()
    return render(request, 'app/agregar_cita.html', {'form': form})

def agregar_notificacion(request):
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = NotificacionForm()
    return render(request, 'app/agregar_notificacion.html', {'form': form})