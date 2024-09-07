# Generated by Django 4.2.15 on 2024-09-06 14:10

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_alter_contenido_cuerpo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contenido',
            old_name='numero_valoraciones',
            new_name='cantidad_dislikes',
        ),
        migrations.RenameField(
            model_name='contenido',
            old_name='numero_vistas',
            new_name='cantidad_likes',
        ),
        migrations.AddField(
            model_name='contenido',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenido',
            name='cantidad_valoraciones',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='cantidad_vistas',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='fecha_publicacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='contenido',
            name='resumen',
            field=models.TextField(default='resumen'),
        ),
        migrations.AddField(
            model_name='contenido',
            name='vigencia',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='imagen',
            field=models.ImageField(default=None, null=True, upload_to='content'),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('resumen', models.TextField()),
                ('cuerpo', ckeditor_uploader.fields.RichTextUploadingField()),
                ('fecha_publicacion', models.DateField(default=datetime.date.today)),
                ('vigencia', models.DateField(default=datetime.date.today)),
                ('fecha_version', models.DateTimeField(default=django.utils.timezone.now)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versiones', to='content.contenido')),
            ],
            options={
                'ordering': ['-fecha_version'],
            },
        ),
    ]