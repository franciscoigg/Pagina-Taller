from django.shortcuts import render,redirect,get_object_or_404
from app.forms import AgregarCitaForm, ClienteForm, CitaForm,UserRegistrationForm,UserLoginForm, TatuadorForm, EditarTatuadorForm
from app.models import Tatuador,Cita,EstadoCita,Cliente
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from datetime import datetime


# procedure

from django.db import connection

def obtener_clientes_por_tatuador(tatuador_id):
    with connection.cursor() as cursor:
        cursor.callproc('obtener_clientes_por_tatuador', [tatuador_id])
        
        resultados = cursor.fetchall()
    

    clientes = []
    for row in resultados:
        cliente = {
            'nombre': row[0],
            'email': row[1],
            'telefono': row[2],
            'fecha': row[3],
            'hora': row[4]
        }
        clientes.append(cliente)
    
    return clientes

def obtener_citas_cliente(cliente_id):
    with connection.cursor() as cursor:

        cursor.callproc('obtener_citas_cliente', [cliente_id])
        resultados = cursor.fetchall()
        

    citas = []
    for row in resultados:
        cita = {
            'cita_id': row[0],
            'fecha': row[1],
            'hora': row[2],
            'estado_nombre': row[3],
            'tatuador_nombre': row[4]
        }

        try:
            estado = EstadoCita.objects.get(nombre=cita['estado_nombre'])
            cita['estado_nombre'] = estado.nombre 
        except EstadoCita.DoesNotExist:
            
            cita['estado_nombre'] = 'Estado desconocido'

        citas.append(cita)
    
    return citas

def actualizar_estado_cita(cita_id, nuevo_estado_id):
    with connection.cursor() as cursor:
        # Llamar al procedimiento almacenado en la base de datos
        cursor.callproc('actualizar_estado_cita', [cita_id, nuevo_estado_id])

def insertar_cita(cliente_id, tatuador_id, fecha, hora, estado_id):
    with connection.cursor() as cursor:
        cursor.callproc('insertar_cita', [cliente_id, tatuador_id, fecha, hora, estado_id])


# login
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        cliente_form = ClienteForm(request.POST)

        if user_form.is_valid() and cliente_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email'] 
            user.set_password(user_form.cleaned_data['password'])
            user.save()

           
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.email = user_form.cleaned_data['email']
            cliente.save()

            # Iniciar sesión
            login(request, user)

            return redirect('inicio')
    else:
        user_form = UserRegistrationForm()
        cliente_form = ClienteForm()
    
    return render(request, 'registration/registro.html', {'user_form': user_form, 'cliente_form': cliente_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, "Correo o contraseña inválidos")
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('inicio')
#-----

@login_required
def mis_citas(request):
    cliente_id = request.user.cliente.cliente_id
    fecha_filtrada = request.GET.get('fecha')  # Obtener la fecha seleccionada

    # Filtrar las citas por fecha si es proporcionada
    if fecha_filtrada:
        citas = Cita.objects.filter(cliente__cliente_id=cliente_id, fecha=fecha_filtrada).order_by('-fecha', '-hora')
    else:
        citas = Cita.objects.filter(cliente__cliente_id=cliente_id).order_by('-fecha', '-hora')

    return render(request, 'app/mis_citas.html', {'citas': citas, 'fecha_filtrada': fecha_filtrada})

@login_required
def cancelar_cita_cliente(request, cita_id):
    cita = get_object_or_404(Cita, cita_id=cita_id)
    
    # Verificar que el cliente logueado sea el que tiene la cita
    if cita.cliente == request.user.cliente:
        cancelado = EstadoCita.objects.get(nombre="Cancelada")
        cita.estado = cancelado
        cita.save()
        # Opcional: enviar un correo de notificación al tatuador
        enviar_notificacion_cancelacion(cita)
        return redirect('mis_citas')
    else:
        return redirect('inicio')  # O puedes mostrar un mensaje de error

@require_POST
def editar_cita_cliente(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.fecha = request.POST.get('fecha')
    cita.hora = request.POST.get('hora')
    cita.save()
    return redirect('solicitar_cita')

def enviar_notificacion_cancelacion(cita):
    if cita.tatuador and cita.tatuador.email:
        mensaje = (
            f"Estimado {cita.tatuador.nombre},\n\n"
            f"La cita solicitada para {cita.cliente.nombre} el {cita.fecha} a las {cita.hora} ha sido cancelada.\n"
            "Por favor, actualiza tu agenda.\n\n"
            "Saludos,\nEquipo de Perla Negra Ink"
        )
        send_mail(
            'Cancelación de Cita',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [cita.tatuador.email],
            fail_silently=False,
        )    

@login_required
def solicitar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            
            tatuador = cita.tatuador
            if tatuador.disponibilidad == 'No disponible':
                form.add_error('tatuador', 'Este tatuador no está disponible.')
                return render(request, 'app/solicitar_cita.html', {'form': form})

            cita.cliente = request.user.cliente
            estado_solicitada = EstadoCita.objects.get(nombre="Solicitada")
            cita.estado = estado_solicitada
            cita.save()
            
        
            notificar_tatuador(cita)
            return redirect('mis_citas')
    else:
        form = CitaForm()
    
    return render(request, 'app/solicitar_cita.html', {'form': form})

def notificar_tatuador(cita):
    if cita.tatuador and cita.tatuador.email:
        mensaje = (
            f"Estimado {cita.tatuador.nombre},\n\n"
            f"Tienes una nueva cita solicitada por {cita.cliente.nombre}.\n"
            f"Fecha y hora: {cita.fecha} a las {cita.hora}.\n"
            "Por favor, revisa tu agenda y confirma la disponibilidad.\n\n"
            "Saludos,\nEquipo de Perla Negra Ink"
        )
        send_mail(
            'Nueva Solicitud de Cita',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [cita.tatuador.email],
            fail_silently=False,
        )

def privacidad(request):
    return render(request,'app/privacidad.html')

def terminos(request):
    return render(request,'app/terminos.html')

def index(request):
    current_year = datetime.now().year
    return render(request, 'app/index.html', {'current_year': current_year})

@login_required
def lista_citas(request):
    # Obtener el parámetro de fecha del filtro
    fecha_filtrada = request.GET.get('fecha')

    # Verificar si el usuario tiene un tatuador asociado
    if hasattr(request.user, 'tatuador'):
        tatuador = request.user.tatuador
        
        # Filtrar las citas por fecha si se proporciona, de lo contrario mostrar todas las citas
        if fecha_filtrada:
            citas = Cita.objects.filter(tatuador=tatuador, fecha=fecha_filtrada).order_by('-hora')
        else:
            citas = Cita.objects.filter(tatuador=tatuador).order_by('-fecha', '-hora')
        
        print(f"Citas encontradas para el tatuador {tatuador.user.username}: {citas}")
    else:
        citas = Cita.objects.none()  # Si el usuario no tiene un tatuador asociado
        print("El usuario no tiene un tatuador asociado")
    
    # Retornar las citas al template, incluyendo la fecha filtrada
    return render(request, 'app/citas.html', {'citas': citas, 'fecha_filtrada': fecha_filtrada})

@login_required
def cancelar_cita_admin(request, cita_id):
    cita = get_object_or_404(Cita, cita_id=cita_id)
    cancelado = EstadoCita.objects.get(nombre="Cancelada")
    cita.estado = cancelado
    cita.save()
    return redirect('citas')

@login_required
def confirmar_cita(request, cita_id):
    cita = get_object_or_404(Cita, cita_id=cita_id)
    confirmado = EstadoCita.objects.get(nombre="Confirmada") 
    cita.estado = confirmado
    cita.save()

    send_mail(
        'Confirmación de Cita',
        f'Tu cita ha sido confirmada para el {cita.fecha} a las {cita.hora}.',
        settings.DEFAULT_FROM_EMAIL,
        [cita.cliente.email],
        fail_silently=False,
    )

    return redirect('citas')

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def editar_tatuador(request, tatuador_id):
    tatuador = get_object_or_404(Tatuador, tatuador_id=tatuador_id)

    if request.method == 'POST':
        form = EditarTatuadorForm(request.POST, instance=tatuador)
        if form.is_valid():
            form.save()
            return redirect('tatuadores') 
    else:
        form = EditarTatuadorForm(instance=tatuador)

    return render(request, 'app/editar.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def eliminar_tatuador(request, tatuador_id):
    tatuador = get_object_or_404(Tatuador, tatuador_id=tatuador_id)
    if tatuador.user:
        tatuador.user.delete()
    
    if Cita.objects.filter(tatuador=tatuador).exists():
        return redirect('tatuadores')  
        
    tatuador.delete()
    return redirect('tatuadores')

@login_required
@user_passes_test(is_superuser)
def agregar_tatuador(request):
    if request.method == 'POST':
        form = TatuadorForm(request.POST)
        if form.is_valid():
            tatuador = form.save(commit=False)
            
            user = User.objects.create_user(username=tatuador.email, email=tatuador.email, password="123")
            user.is_staff = True
            tatuador.user = user
            tatuador.save()

            return redirect('tatuadores')
    else:
        form = TatuadorForm()
    
    return render(request, 'app/agregar_tatuador.html', {'form': form})

def tatuadores(request):
    tatuadores = Tatuador.objects.all() 
    return render(request, 'app/tatuadores.html', {'tatuadores': tatuadores})

@login_required
@user_passes_test(is_superuser)
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.user:
                user = User.objects.create_user(username=cliente.email, email=cliente.email, password="123")
                cliente.user = user
            cliente.save()

            return redirect('inicio')
    else:
        form = ClienteForm()

    return render(request, 'app/agregar_cliente.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def agregar_cita(request):
    if request.method == 'POST':
        print(request.POST)  
        form = AgregarCitaForm(request.POST)
        if form.is_valid():
            cita=form.save(commit=False)
            cita.save()

            send_mail(
                'Confirmación de Cita',
                f'Tu cita ha sido creada para el  {cita.fecha} a las {cita.hora}.',
                settings.EMAIL_HOST_USER,
                [cita.cliente.email], 
                fail_silently=False,
            )

            return redirect('citas')
        else:
            print(form.errors) 
    else:
        form = AgregarCitaForm()
    return render(request, 'app/agregar_cita.html', {'form': form})


def contactanos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Enviar el mensaje por email
        send_mail(
            f'{nombre} quiere formar parte del equipo ({email})',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            ['fraanciscoigg@gmail.com'],
            fail_silently=False,
        )

    return render(request, 'app/contactanos.html')