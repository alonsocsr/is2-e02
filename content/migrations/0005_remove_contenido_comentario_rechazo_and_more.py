# Generated by Django 4.2.15 on 2024-09-08 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_contenido_comentario_rechazo_version_editor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenido',
            name='comentario_rechazo',
        ),
        migrations.AddField(
            model_name='contenido',
            name='mensaje_rechazo',
            field=models.TextField(blank=True, default=''),
        ),
    ]
