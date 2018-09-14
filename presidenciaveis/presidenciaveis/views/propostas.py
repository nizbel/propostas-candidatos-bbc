# -*- coding: utf-8 -*-
import json

from django.http.response import HttpResponse
from django.template.response import TemplateResponse

from presidenciaveis.presidenciaveis.models.candidatos import Proposta


def ver_propostas(request):
    return TemplateResponse(request, 'propostas.html')

def listar_propostas(request):
    propostas = [{'texto': proposta.texto, 'candidato': proposta.candidato_id, 'area': proposta.area.nome, 'id': proposta.id} \
                 for proposta in Proposta.objects.all().select_related('area')]
    return HttpResponse(json.dumps(propostas), content_type = "application/json")   
