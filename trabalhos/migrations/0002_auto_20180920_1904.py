# Generated by Django 2.0.8 on 2018-09-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trabalhos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='areatema',
            options={'ordering': ('nome',), 'verbose_name': 'área/tema', 'verbose_name_plural': 'áreas/temas'},
        ),
        migrations.AlterModelOptions(
            name='modalidade',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='trabalho',
            options={'ordering': ('titulo',)},
        )
    ]