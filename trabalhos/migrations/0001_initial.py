# Generated by Django 2.0.8 on 2018-08-09 23:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Definicoes',
            fields=[
                ('evento', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='def_trabalhos', serialize=False, to='eventos.Evento')),
                ('prazo', models.DateTimeField(default=django.utils.timezone.now, verbose_name='prazo para submissão')),
                ('submeter_poster', models.BooleanField(default=False, verbose_name='habilitar submissão de poster')),
                ('modelo_poster', models.FileField(blank=True, null=True, upload_to='modelos/poster', verbose_name='Modelo de Poster')),
                ('submeter_mostra', models.BooleanField(default=False, verbose_name='habilitar submissão de mostra tecnologica')),
                ('modelo_plano_pesquisa', models.FileField(blank=True, null=True, upload_to='modelos/plano_pesquisa', verbose_name='Modelo de Plano de pesquisa')),
                ('modelo_relatorio', models.FileField(blank=True, null=True, upload_to='modelos/relatorio', verbose_name='Modelo de Relatório')),
                ('modelo_resumo', models.FileField(blank=True, null=True, upload_to='modelos/resumo', verbose_name='Modelo de Resumo')),
            ],
            options={
                'verbose_name': 'definição de trabalhos',
                'verbose_name_plural': 'definições de trabalhos',
            },
        ),
        migrations.CreateModel(
            name='MostraTecnologica',
            fields=[
                ('inscricao_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='eventos.Inscricao')),
                ('titulo', models.CharField(max_length=255, verbose_name='título')),
                ('nome_autor', models.CharField(max_length=255, verbose_name='nome completo do autor principal')),
                ('cpf_autor', models.CharField(max_length=11, verbose_name='CPF do autor principal')),
                ('nome_orientador', models.CharField(max_length=255, verbose_name='nome completo do orientador')),
                ('cpf_orientador', models.CharField(max_length=11, verbose_name='CPF do orientador')),
                ('aprovado', models.BooleanField(default=False, editable=False)),
                ('plano_pesquisa', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='plano de pesquisa')),
                ('relatorio_projeto', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='relatório do projeto')),
                ('resumo_projeto', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='resumo do projeto')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trabalhos.Area', verbose_name='área de interesse')),
            ],
            options={
                'abstract': False,
            },
            bases=('eventos.inscricao',),
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('inscricao_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='eventos.Inscricao')),
                ('titulo', models.CharField(max_length=255, verbose_name='título')),
                ('nome_autor', models.CharField(max_length=255, verbose_name='nome completo do autor principal')),
                ('cpf_autor', models.CharField(max_length=11, verbose_name='CPF do autor principal')),
                ('nome_orientador', models.CharField(max_length=255, verbose_name='nome completo do orientador')),
                ('cpf_orientador', models.CharField(max_length=11, verbose_name='CPF do orientador')),
                ('aprovado', models.BooleanField(default=False, editable=False)),
                ('resumo_expandido', models.FileField(upload_to='trabalhos/posters')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trabalhos.Area', verbose_name='área de interesse')),
            ],
            options={
                'abstract': False,
            },
            bases=('eventos.inscricao',),
        ),
    ]
