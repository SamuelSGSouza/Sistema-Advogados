# Generated by Django 4.2.6 on 2023-10-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0010_termosemailadvogados'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermoNegativoNomeAdvogado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termo', models.CharField(max_length=255, verbose_name='Termo de Remoção')),
                ('fase', models.CharField(default='Fase 3', max_length=255, verbose_name='Fase')),
            ],
        ),
    ]
