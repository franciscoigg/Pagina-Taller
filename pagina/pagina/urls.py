"""pagina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='inicio'),
    path('registro/', views.register, name='registro'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('solicitar_cita/', views.solicitar_cita, name='solicitar_cita'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita_admin, name='cancelar_cita_admin'),
    path('cancelar_cita_cliente/<int:cita_id>/', views.cancelar_cita_cliente, name='cancelar_cita_cliente'),
    path('citas/editar/<int:cita_id>/', views.editar_cita_cliente, name='editar_cita_cliente'),
    path('mis_citas/', views.mis_citas, name='mis_citas'),
    path('confirmar_cita/<int:cita_id>/', views.confirmar_cita, name='confirmar_cita'),
    path('tatuadores/',views.tatuadores,name='tatuadores'),
    path('citas/',views.lista_citas,name='citas'),
    path('terminos/', views.terminos, name='terminos'),
        path('privacidad/', views.privacidad, name='privacidad'),
#   path('agregar_tatuador/', views.agregar_tatuador, name='agregar_tatuador'),
#   path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('agregar_cita/', views.agregar_cita, name='agregar_cita'),
    path('contactanos/', views.contactanos, name='contactanos'),
]
