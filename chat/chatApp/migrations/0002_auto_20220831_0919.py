# Generated by Django 3.0.5 on 2022-08-31 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='role',
            table='role',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
        migrations.AlterModelTable(
            name='userrole',
            table='userrole',
        ),
    ]
