# Generated by Django 2.0.8 on 2018-08-20 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='pagamento',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Pago'), (2, 'Recusado')], default=0),
        ),
    ]
