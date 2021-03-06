# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presidenciaveis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20, verbose_name='\xc1rea')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='candidato',
            unique_together=set([('nome',)]),
        ),
        migrations.AlterUniqueTogether(
            name='area',
            unique_together=set([('nome',)]),
        ),
        migrations.AddField(
            model_name='proposta',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='presidenciaveis.Area'),
            preserve_default=False,
        ),
    ]
