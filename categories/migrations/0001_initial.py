# Generated by Django 5.1 on 2024-08-27 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.TextField(max_length=100)),
                ('descripcion_corta', models.CharField(max_length=10)),
                ('estado', models.BooleanField(default=True)),
                ('moderada', models.BooleanField(default=False)),
                ('tipo_categoria', models.CharField(choices=[('PU', 'Pública'), ('GR', 'Gratuita'), ('PA', 'Paga')], default='PU', max_length=3)),
                ('precio', models.IntegerField(default=20000, help_text='Precio solo aplicable si la categoría es paga.', null=True)),
            ],
        ),
    ]
