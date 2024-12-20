# Generated by Django 3.2 on 2024-12-02 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoCita',
            fields=[
                ('estado_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tatuador',
            fields=[
                ('tatuador_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, null=True)),
                ('especialidad', models.CharField(max_length=30, null=True)),
                ('disponibilidad', models.CharField(choices=[('Disponible', 'Disponible'), ('No disponible', 'No disponible')], default='Disponible', max_length=20)),
                ('telefono', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('cliente_id', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('email', models.EmailField(max_length=30, null=True, unique=True)),
                ('nombre', models.CharField(max_length=40, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('cita_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=True)),
                ('hora', models.TimeField(null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cliente')),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.estadocita')),
                ('tatuador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tatuador')),
            ],
        ),
    ]
