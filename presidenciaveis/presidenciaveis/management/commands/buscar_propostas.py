# -*- coding: utf-8 -*-
import re
from urllib2 import Request, urlopen, HTTPError, URLError

from django.core.management.base import BaseCommand
from django.db import transaction

from presidenciaveis.presidenciaveis.models.candidatos import Area, Candidato, \
    Proposta


class Command(BaseCommand):
    help = 'Busca propostas dos presidenciáveis'

    def handle(self, *args, **options):
        bbc_url = 'https://www.bbc.com/portuguese/brasil-45215784'
        req = Request(bbc_url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError as e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
            data = response.read()
            inicio = data.find('panel-two-content')
            fim = data.rfind('<style>', inicio)
            parte_util = data[inicio:fim]
            print parte_util
            
            
            try:
                with transaction.atomic():
                    areas = re.findall('<h2>(.*?)</h2>', parte_util)
                    print u'Áreas'
                    for area in areas:
                        area = area.strip()
                        print area
                        if not Area.objects.filter(nome=area).exists():
                            Area.objects.create(nome=area)
                    
                    proposta_areas = re.findall('<h2>(.*?)(?=<h2>|\Z)', parte_util, re.DOTALL)
                    if len(proposta_areas) != 6:
                        raise ValueError('erro na quantidade de areas')
                    
                    for proposta_area in proposta_areas:
                        # Buscar área atual
                        area_atual = Area.objects.get(nome=proposta_area[:proposta_area.find('</h2>')].strip())
                        
                        # Buscar candidato caso não exista
                        candidatos = re.findall('party-content(.*?)(?=</ul>|\Z)', proposta_area, re.DOTALL)
                        
                        for candidato in candidatos:
                            dados_candidato = re.findall('<span class="header"><span class="header-bold">(.*?)</span> (.*?)</span>', candidato, re.DOTALL)
#                             print dados_candidato
                            nome_candidato, partido = dados_candidato[0]
                            nome_candidato = nome_candidato.strip()
                            partido = partido.strip()
                            if not Candidato.objects.filter(nome=nome_candidato).exists():
                                Candidato.objects.create(nome=nome_candidato, numero=0, partido=partido)
                            
                            candidato_atual = Candidato.objects.get(nome=nome_candidato)
                            propostas = re.findall('<li>(.*?)</li>', candidato, re.DOTALL)
                            for proposta in propostas:
                                proposta = proposta.strip().replace('&quot;', '"')
                                if proposta == 'Sem dados até o momento':
                                    continue
#                                 print proposta
                                if not Proposta.objects.filter(texto=proposta, candidato=candidato_atual).exists():
                                    Proposta.objects.create(texto=proposta, candidato=candidato_atual, area=area_atual)
            except:
                raise
            
            
#             <span class="header"><span class="header-bold">(.*?)</span> (.*?)</span>