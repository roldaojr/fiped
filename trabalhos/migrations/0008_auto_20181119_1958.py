# Generated by Django 2.0.8 on 2018-11-19 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trabalhos', '0007_auto_20181022_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabalho',
            name='carta_aceite',
            field=models.FileField(blank=True, null=True, upload_to='cartas-de-aceite', verbose_name='Carta de aceite'),
        ),
    ]
