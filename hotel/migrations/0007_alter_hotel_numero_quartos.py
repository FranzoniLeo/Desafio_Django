# Generated by Django 5.2 on 2025-04-17 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_hotel_numero_quartos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='numero_quartos',
            field=models.IntegerField(default=0),
        ),
    ]
