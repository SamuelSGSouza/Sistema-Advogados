# Generated by Django 4.2.6 on 2023-10-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0005_statusfase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusfase',
            name='status',
            field=models.CharField(max_length=255, verbose_name='Status'),
        ),
    ]
