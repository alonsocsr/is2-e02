# Generated by Django 4.2.15 on 2024-11-01 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_alter_categorias_prioridad'),
        ('profiles', '0009_profile_contenidos_dislike_profile_contenidos_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='suscripciones',
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('monto', models.IntegerField(null=True)),
                ('medio_pago', models.CharField(max_length=2, choices=[
                    ('TC', 'Tarjeta de Crédito'),
                    ('TD', 'Tarjeta de Débito'),
                    ('PP', 'PayPal'),
                    ('TR', 'Transferencia Bancaria'),
                ])),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.categorias')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suscripciones', to='profiles.profile')),
            ],
            options={
                'unique_together': {('profile', 'categoria')},
            },
        ),
    ]