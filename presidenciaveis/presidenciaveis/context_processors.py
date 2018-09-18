# -*- coding: utf-8 -*-
from django.conf import settings

def DEBUG(context):
    return {'DEBUG': settings.DEBUG}

