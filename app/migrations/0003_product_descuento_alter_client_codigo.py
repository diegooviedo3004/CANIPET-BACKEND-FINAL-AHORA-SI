# Generated by Django 4.1.3 on 2022-11-24 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product_promocionar_a_alter_client_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='2YIV5PQ', editable=False, max_length=7, null=True),
        ),
    ]
