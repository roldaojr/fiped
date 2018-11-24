# Generated by Django 2.0.8 on 2018-11-20 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0006_auto_20180920_1904'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oficinas', '0006_mesaredonda_inscricoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seminario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('arquivo', models.FileField(upload_to='seminarios')),
                ('vagas', models.IntegerField(default=0)),
                ('situacao', models.IntegerField(choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Reprovado')], default=0, editable=False, verbose_name='situação')),
                ('inscricoes', models.ManyToManyField(blank=True, editable=False, related_name='seminarios', to='eventos.Inscricao')),
                ('ministrante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seminarios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'seminário temático',
                'verbose_name_plural': 'seminários temáticos',
                'ordering': ('nome',),
            },
        ),
    ]