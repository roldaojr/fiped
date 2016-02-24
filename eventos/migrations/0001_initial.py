# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='nome')),
                ('local', models.CharField(max_length=255, null=True, blank=True)),
                ('tipo', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=255, verbose_name='nome')),
                ('data_inicial', models.DateField(verbose_name='data inicial')),
                ('data_final', models.DateField(verbose_name='data final')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField()),
                ('hora_inicial', models.TimeField()),
                ('hora_final', models.TimeField()),
                ('atividade', models.ForeignKey(related_name='horarios', to='eventos.Atividade')),
            ],
            options={
                'ordering': ('data', 'hora_inicial', 'hora_final'),
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('espera', models.BooleanField(default=False, editable=False)),
                ('atividade', models.ForeignKey(related_name='inscricoes', editable=False, to='eventos.Atividade')),
                ('usuario', models.ForeignKey(related_name='inscricoes', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'inscri\xe7\xe3o',
                'verbose_name_plural': 'inscri\xe7\xf5es',
            },
        ),
        migrations.AlterUniqueTogether(
            name='inscricao',
            unique_together=set([('atividade', 'usuario')]),
        ),
    ]
