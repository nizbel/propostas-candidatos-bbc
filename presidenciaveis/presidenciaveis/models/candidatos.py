# -*- coding: utf-8 -*-
from django.db import models


class Candidato(models.Model):
    nome = models.CharField(u'Nome do candidato', max_length=30)
    numero = models.SmallIntegerField(u'Número do candidato')
    partido = models.CharField(u'Nome do partido', max_length=10)
    
    class Meta:
        unique_together=('nome',)
    
class Proposta(models.Model):
    texto = models.CharField(u'Texto da proposta', max_length=1000)
    candidato = models.ForeignKey('Candidato')
    area = models.ForeignKey('Area')
    
    class Meta:
        unique_together=('texto', 'candidato')
    
class Area(models.Model):
    nome = models.CharField(u'Área', max_length=50)
    
    class Meta:
        unique_together=('nome',)