# -*- coding: utf-8 -*-
import os
from django.conf.urls import patterns
from django.conf import settings
from apps.nextify.views import NextifyUtils

urlpatterns = []

nextify_utils = NextifyUtils()
for i in nextify_utils.get_url_list():
    try:
        urlpatterns=urlpatterns+patterns('',
            (r'^%s/(?P<id>[\d]+)/files$' % i, 'apps.nextify.views.index', {'page': i, 'action': 'file'}),
            (r'^%s/static/(?P<path>.*)$' % i, 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static/nextify') }),
                                
            (r'^%s/(?P<action>\w+)/(?P<element>\w+)$' % i, 'apps.nextify.views.index', {'page':i}),
            (r'^%s/(?P<action>[\w-]+)$' % i, 'apps.nextify.views.index', {'page':i}),
            (r'^%s/' % i, 'apps.nextify.views.index', {'page':i}),
        )
    except:
        print('Aadressi laadimine ebaõnnestus')
