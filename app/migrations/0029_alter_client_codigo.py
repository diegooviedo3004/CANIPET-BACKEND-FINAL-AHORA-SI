# Generated by Django 4.1.3 on 2023-07-04 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_paciente_foto_alter_client_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='LVOPLG2', editable=False, max_length=7, null=True),
        ),
    ]
