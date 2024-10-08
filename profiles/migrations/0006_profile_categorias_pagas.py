# Generated by Django 4.2.15 on 2024-09-11 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_alter_categorias_prioridad'),
        ('profiles', '0005_profile_categorias_interes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='categorias_pagas',
            field=models.ManyToManyField(blank=True, limit_choices_to={'tipo_categoria': 'PA'}, related_name='categorias_pagas', to='categories.categorias'),
        ),
    ]
