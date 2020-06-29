# -*- coding: utf-8 -*-
from django.contrib import admin
from presidenciaveis.presidenciaveis.models.candidatos import Candidato,\
    Concordancia, Proposta


admin.site.register(Candidato)

class ConcordanciaAdmin(admin.ModelAdmin):
    search_fields = ['nome_candidato', 'texto_proposta', 'data_hora']
    # TODO adicionar Tags
    list_display = ('texto_proposta', 'nome_candidato', 'data_hora', 'nivel')
    
admin.site.register(Concordancia, ConcordanciaAdmin)

class PropostaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'nome_candidato', 'resultado_positivo', 'resultado_negativo', 'resultado_neutro', 'qtd_concordancias')
    
admin.site.register(Proposta, PropostaAdmin)