# Generated by Django 4.2.6 on 2023-11-06 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_orederdetails_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orederdetails',
            name='total_price',
        ),
    ]
