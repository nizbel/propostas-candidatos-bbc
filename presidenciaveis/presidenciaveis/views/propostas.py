# -*- coding: utf-8 -*-
import json

from django.http.response import HttpResponse
from django.template.response import TemplateResponse

from presidenciaveis.presidenciaveis.models.candidatos import Proposta, \
    Candidato


def ver_propostas(request):
    return TemplateResponse(request, 'propostas.html')

def listar_propostas(request):
    propostas = [{'texto': proposta.texto, 'candidato': proposta.candidato_id, 'area': proposta.area.nome, 'id': proposta.id} \
                 for proposta in Proposta.objects.all().select_related('area')]
    return HttpResponse(json.dumps(propostas), content_type = "application/json")   

def listar_candidatos(request):
    candidatos = [{'nome': candidato.nome, 'numero': candidato.numero, 'partido': candidato.partido, 'id': candidato.id} \
                 for candidato in Candidato.objects.all()]
    return HttpResponse(json.dumps(candidatos), content_type = "application/json")  