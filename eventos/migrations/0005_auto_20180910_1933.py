# Generated by Django 2.0.8 on 2018-09-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_inscricao_desconto'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='validado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tipoinscricao',
            name='validar',
            field=models.BooleanField(default=False, help_text='Validar inscrição desse tipo'),
        ),
    ]
