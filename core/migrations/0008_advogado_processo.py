# Generated by Django 4.2.6 on 2023-10-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_advogado_data_atualiacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='advogado',
            name='processo',
            field=models.CharField(default='teste', max_length=20, verbose_name='Processo'),
            preserve_default=False,
        ),
    ]
