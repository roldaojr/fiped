# Generated by Django 2.0.8 on 2018-09-25 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trabalhos', '0003_auto_20180920_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabalho',
            name='observacoes',
            field=models.TextField(blank=True, null=True, verbose_name='observações'),
        ),
    ]