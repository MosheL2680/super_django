# Generated by Django 4.2.6 on 2023-11-06 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_orederdetails_total_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrederDetails',
            new_name='OrederDetail',
        ),
    ]
