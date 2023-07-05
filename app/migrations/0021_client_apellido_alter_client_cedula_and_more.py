# Generated by Django 4.1.3 on 2023-07-03 00:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_client_cedula_alter_client_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='apellido',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='cedula',
            field=models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='La cédula no tiene el formato correcto (Ejemplo: 001-030725-1040G)', regex='^\\d{3}-\\d{6}-\\d{4}[A-Z]$')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='I799WQQ', editable=False, max_length=7, null=True),
        ),
    ]
