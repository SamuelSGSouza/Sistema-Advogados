# Generated by Django 4.2.6 on 2023-10-23 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_advogado_oab'),
    ]

    operations = [
        migrations.AddField(
            model_name='advogado',
            name='tratamento',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tratamento'),
        ),
    ]