# Generated by Django 4.2.6 on 2023-10-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0006_alter_statusfase_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomesMasculinos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome Masculino')),
                ('fase', models.CharField(default='Fase 3', max_length=255, verbose_name='Fase')),
            ],
        ),
    ]
