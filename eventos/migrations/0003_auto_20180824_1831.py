# Generated by Django 2.0.8 on 2018-08-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_inscricao_pagamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipoinscricao',
            options={'verbose_name': 'tipo de inscrição', 'verbose_name_plural': 'tipos de inscrição'},
        ),
        migrations.AddField(
            model_name='tipoinscricao',
            name='limite',
            field=models.IntegerField(default=0, help_text='0 para ilimitado'),
        ),
    ]
