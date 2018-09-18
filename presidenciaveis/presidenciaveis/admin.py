# -*- coding: utf-8 -*-
from django.contrib import admin
from presidenciaveis.presidenciaveis.models.candidatos import Candidato,\
    Concordancia, Proposta


admin.site.register(Candidato)

admin.site.register(Concordancia)

admin.site.register(Proposta)