# Generated by Django 5.1 on 2024-09-01 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_alter_categorias_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorias',
            name='moderada',
            field=models.BooleanField(default=True),
        ),
    ]
