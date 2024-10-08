# Generated by Django 4.2.15 on 2024-09-07 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0003_rename_numero_valoraciones_contenido_cantidad_dislikes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='comentario_rechazo',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='version',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='resumen',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='titulo',
            field=models.CharField(default='', max_length=200),
        ),
    ]
