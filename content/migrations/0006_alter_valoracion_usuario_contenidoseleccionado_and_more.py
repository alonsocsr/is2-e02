# Generated by Django 4.2.15 on 2024-09-08 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0005_remove_contenido_comentario_rechazo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valoracion',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ContenidoSeleccionado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.contenido')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='ContenidoReportado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(choices=[('odio', 'Mensaje de Odio'), ('acoso', 'Acoso'), ('privacidad', 'Privacidad'), ('difamacion', 'Difamación'), ('spam', 'Spam')], default='spam', max_length=50)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.contenido')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
