# Generated by Django 3.1.4 on 2020-12-03 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_transaccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='dinero_ganado',
        ),
        migrations.RemoveField(
            model_name='club',
            name='dinero_invertido',
        ),
    ]