# Generated by Django 2.0.8 on 2018-10-19 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficinas', '0003_auto_20180920_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('editora', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=100, verbose_name='ISBN')),
                ('ano', models.IntegerField()),
                ('autores', models.CharField(max_length=100)),
                ('biografia', models.TextField()),
                ('resumo', models.TextField()),
                ('palavras_chave', models.CharField(max_length=100)),
                ('paginas', models.IntegerField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='preço')),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, verbose_name='e-mail')),
                ('capa', models.FileField(upload_to='livros')),
                ('situacao', models.IntegerField(choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Reprovado')], default=0, editable=False, verbose_name='situação')),
            ],
        ),
    ]
