# Generated by Django 4.2.6 on 2023-10-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_processo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo',
            name='paginas',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Páginas'),
        ),
    ]