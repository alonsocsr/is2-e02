# Generated by Django 4.2.15 on 2024-09-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_alter_valoracion_usuario_contenidoseleccionado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidoreportado',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
    ]