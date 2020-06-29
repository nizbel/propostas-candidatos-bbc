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
        
    def nome_candidato(self):
        return self.candidato.nome
    
    def qtd_concordancias(self):
        return Concordancia.objects.filter(proposta=self).count()
    
    def qtd_concordancias_positivas(self):
        return Concordancia.objects.filter(proposta=self, nivel=1).count()
    def qtd_concordancias_negativas(self):
        return Concordancia.objects.filter(proposta=self, nivel=-1).count()
    def qtd_concordancias_neutras(self):
        return Concordancia.objects.filter(proposta=self, nivel=0).count()
    
    def percentual_positivo(self):
        return float(self.qtd_concordancias_positivas()) / self.qtd_concordancias() * 100
    def percentual_negativo(self):
        return float(self.qtd_concordancias_negativas()) / self.qtd_concordancias() * 100
    def percentual_neutro(self):
        return float(self.qtd_concordancias_neutras()) / self.qtd_concordancias() * 100
    
    def resultado_positivo(self):
        return '%s (%.2f%%)' % (self.qtd_concordancias_positivas(), self.percentual_positivo())
    def resultado_negativo(self):
        return '%s (%.2f%%)' % (self.qtd_concordancias_negativas(), self.percentual_negativo())
    def resultado_neutro(self):
        return '%s (%.2f%%)' % (self.qtd_concordancias_neutras(), self.percentual_neutro())
    
class Area(models.Model):
    nome = models.CharField(u'Área', max_length=50)
    
    class Meta:
        unique_together=('nome',)
        
class Concordancia(models.Model):
    data_hora = models.DateTimeField(u'Data')
    proposta = models.ForeignKey('Proposta')
    nivel = models.SmallIntegerField(u'Nível de concordância')
    
    def nome_candidato(self):
        return self.proposta.candidato.nome
    
    def texto_proposta(self):
        return self.proposta.texto
    