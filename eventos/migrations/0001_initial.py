# Generated by Django 2.0.8 on 2018-08-14 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('local', models.CharField(blank=True, max_length=255, null=True)),
                ('modalidade', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora_inicial', models.TimeField()),
                ('hora_final', models.TimeField()),
                ('atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='eventos.Atividade')),
            ],
            options={
                'ordering': ('data', 'hora_inicial', 'hora_final'),
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instituicao', models.CharField(blank=True, max_length=100, null=True, verbose_name='instituição')),
                ('titulacao', models.CharField(blank=True, max_length=50, null=True, verbose_name='titulação')),
                ('deficiencia', models.CharField(blank=True, max_length=300, null=True, verbose_name='deficiência')),
                ('endereco', models.CharField(blank=True, max_length=300, null=True, verbose_name='endereço')),
                ('numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='número')),
                ('cidade', models.CharField(blank=True, max_length=50, null=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('alojamento', models.BooleanField(default=False)),
                ('certificado', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name': 'inscrição',
                'verbose_name_plural': 'inscrições',
            },
        ),
        migrations.CreateModel(
            name='TipoInscricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='nome')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='preço')),
            ],
            options={
                'verbose_name': 'tipo de inscrição',
                'verbose_name_plural': 'tipos de inscrições',
            },
        ),
        migrations.AddField(
            model_name='inscricao',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='eventos.TipoInscricao'),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='usuario',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='inscricao', to=settings.AUTH_USER_MODEL),
        ),
    ]
