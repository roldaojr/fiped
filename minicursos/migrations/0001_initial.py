# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Definicoes',
            fields=[
                ('evento', models.OneToOneField(related_name='def_minicursos', primary_key=True, serialize=False, to='eventos.Evento')),
                ('maximo', models.IntegerField(default=1, verbose_name='m\xe1ximo de inscri\xe7\xf5es por pessoa')),
            ],
            options={
                'verbose_name': 'defini\xe7\xe3o de minicurso',
                'verbose_name_plural': 'defini\xe7\xf5es de minicurso',
            },
        ),
        migrations.CreateModel(
            name='Minicurso',
            fields=[
                ('atividade_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='eventos.Atividade')),
                ('descricao', models.TextField(null=True, verbose_name='descri\xe7\xe3o', blank=True)),
                ('pre_requisitos', models.TextField(null=True, verbose_name='pr\xe9-requisitos', blank=True)),
                ('vagas', models.PositiveIntegerField(default=0)),
                ('inscritos', models.PositiveIntegerField(default=0, verbose_name='n\xfamero de inscritos')),
                ('vagas_reserva', models.PositiveIntegerField(default=0)),
                ('inscritos_reserva', models.PositiveIntegerField(default=0, verbose_name='n\xfamero de inscritos na reserva')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=('eventos.atividade',),
        ),
        migrations.CreateModel(
            name='Ministrante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('foto', models.ImageField(null=True, upload_to='fotos/ministrante', blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='minicurso',
            name='ministrante',
            field=models.ForeignKey(to='minicursos.Ministrante'),
        ),
    ]
