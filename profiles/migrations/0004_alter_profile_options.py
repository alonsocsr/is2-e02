# Generated by Django 5.1 on 2024-08-30 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'default_permissions': ()},
        ),
    ]