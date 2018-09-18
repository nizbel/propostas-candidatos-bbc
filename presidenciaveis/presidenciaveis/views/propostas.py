# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.utils import timezone

from presidenciaveis.presidenciaveis.models.candidatos import Proposta, \
    Candidato, Concordancia


def ver_propostas(request):
    return TemplateResponse(request, 'propostas.html')

def enviar_avaliacoes(request):
    try:
        with transaction.atomic():
            data_hora = timezone.now()
            propostas = request.body.split(';')
        
            for proposta in propostas:
                proposta_id = proposta.split(':')[0]
                proposta_concordancia = proposta.split(':')[1]
                
                if not proposta_id.isdigit():
                    raise ValueError('Valor de proposta deve ser numérico')
                
                if not proposta_concordancia in ['-1', '0', '1']:
                    raise ValueError('Valor de concordância deve ser numérico')
                
                Concordancia.objects.create(data_hora=data_hora, proposta_id=int(proposta_id), nivel=int(proposta_concordancia))
        
            return HttpResponse(json.dumps({'sucesso': True}), content_type = "application/json")  
    except Exception as e:
        print e
        return HttpResponse(json.dumps({'sucesso': False}), content_type = "application/json") 

def listar_propostas(request):
    propostas = [{'texto': proposta.texto, 'candidato': proposta.candidato_id, 'area': proposta.area.nome, 'id': proposta.id} \
                 for proposta in Proposta.objects.all().select_related('area')]
    return HttpResponse(json.dumps(propostas), content_type = "application/json")   

def listar_candidatos(request):
    candidatos = [{'nome': candidato.nome, 'numero': candidato.numero, 'partido': candidato.partido, 'id': candidato.id} \
                 for candidato in Candidato.objects.all()]
    return HttpResponse(json.dumps(candidatos), content_type = "application/json")  