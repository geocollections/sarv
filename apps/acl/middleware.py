# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from apps.acl.views import Acl as vAcl
from sarv.local_settings import PROJECT_ADMINS

class PageRightsCheck(object):
    def process_request(self, request):
        if request.path in ("/logout", "/login", "/", ""): 
            return None

        acl = vAcl()
        page = acl.get_page_from_url(request)
        userrights = acl.get_page_user_rights(request)
        
        if "admin+" in page:
            if page == "admin+menu":
                return None
            if hasattr(request, "sarvuser") \
            and request.sarvuser.pk in PROJECT_ADMINS:
                request.__class__.acl = [True,True,True,True]
            elif "admin+acl" in page \
            and "acl" in request.session \
            and page in request.session["acl"] \
            and (userrights[3] == True \
            or request.sarvuser.pk in PROJECT_ADMINS):
                pass
            else:
                return HttpResponseRedirect("/")
            
        if not "acl" in request.session:
            return HttpResponseRedirect("/")
        if "acl" in request.session \
        and page in request.session["acl"] \
        and userrights[0] == False:
            return HttpResponseRedirect("/")
        else:
            request.__class__.acl = userrights
