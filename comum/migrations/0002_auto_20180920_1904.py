# Generated by Django 2.0.8 on 2018-09-20 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ('nome_completo',)},
        ),
    ]
