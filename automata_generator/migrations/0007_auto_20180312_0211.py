# Generated by Django 2.0.2 on 2018-03-12 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automata_generator', '0006_auto_20180227_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automatastate',
            name='label',
            field=models.CharField(help_text='Ingrese la etiqueta del estado. Ej: q0', max_length=10, verbose_name='Etiqueta'),
        ),
    ]
