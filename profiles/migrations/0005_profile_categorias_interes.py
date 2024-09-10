# Generated by Django 4.2.15 on 2024-09-06 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_alter_categorias_moderada'),
        ('profiles', '0004_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='categorias_interes',
            field=models.ManyToManyField(blank=True, related_name='categorias_interes', to='categories.categorias'),
        ),
    ]