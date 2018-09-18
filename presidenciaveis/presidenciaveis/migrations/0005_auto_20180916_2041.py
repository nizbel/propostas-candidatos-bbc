# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-16 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presidenciaveis', '0004_auto_20180914_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concordancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(verbose_name='Data')),
                ('nivel', models.SmallIntegerField(verbose_name='N\xedvel de concord\xe2ncia')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='proposta',
            unique_together=set([('texto', 'candidato')]),
        ),
        migrations.AddField(
            model_name='concordancia',
            name='proposta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='presidenciaveis.Proposta'),
        ),
    ]