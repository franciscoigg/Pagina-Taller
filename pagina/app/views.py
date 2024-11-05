from django.shortcuts import render,redirect,get_object_or_404
from app.forms import AgregarCitaForm, ClienteForm, CitaForm,UserRegistrationForm,UserLoginForm
from app.models import Tatuador,Cita,EstadoCita
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST




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
    citas = Cita.objects.filter(cliente=request.user.cliente).order_by('-fecha', '-hora')
    return render(request, 'app/mis_citas.html', {'citas': citas})

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

def index(request):
    return render(request,'app/index.html')

def lista_citas(request):
    citas = Cita.objects.order_by('-fecha', '-hora') 
    return render(request, 'app/citas.html', {'citas': citas})

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


#def agregar_tatuador(request):
#    if request.method == 'POST':
#        form = TatuadorForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('inicio') 
#    else:
#        form = TatuadorForm()
#    return render(request, 'app/agregar_tatuador.html', {'form': form})

def tatuadores(request):
    tatuadores = Tatuador.objects.all() 
    return render(request, 'app/tatuadores.html', {'tatuadores': tatuadores})


#def agregar_cliente(request):
#    if request.method == 'POST':
#        form = ClienteForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('inicio')
#    else:
#        form = ClienteForm()
#    return render(request, 'app/agregar_cliente.html', {'form': form})

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

