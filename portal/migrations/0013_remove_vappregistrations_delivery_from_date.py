# Generated by Django 4.0.4 on 2023-11-13 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_vappregistrations_delivery_from_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vappregistrations',
            name='delivery_from_date',
        ),
    ]
