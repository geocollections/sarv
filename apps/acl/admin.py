# -*- coding: utf-8 -*-
import json
from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from apps.acl.models import AclRightsGroup, AclGroup
from apps.acl.views import Acl as vAcl
from sarv.settings import PROJECT_ADMINS

from sarv.utils import get_model
User, Page, Menu = get_model(["User", "SarvPage", "SarvMenu"])

class AclAdmin(object):

    def __init__(self):
        pass
        
    def index(self, request):
        rightsgroups = AclRightsGroup.objects.all()
        pagerights, users, column_names = self.get_page_data(request)
        print([pagerights, users, column_names])
        return render_to_response("admin/acl_index.html",
            {"data": json.dumps({
                "pages": pagerights,
                "users": users}),
            "users": users,
            "rightsgroups": rightsgroups,
            "col_names": column_names
            },
            RequestContext(request, {})
        )

    # Route url requests from urls.py to match views.py Acl class methods
    def router(self, request, action=False):
        response = False
        acl = vAcl()
        if "add" and hasattr(acl, request.GET.dict()["subaction"]):
            response = getattr(acl, request.GET.dict()["subaction"])(request.GET.dict())
        else: 
            print ("no attr")
        return HttpResponse(response)
    
    def get_page_data(self, request):
        p_l=Menu.objects \
                .select_related().all() \
                .exclude(page__visibility="public") \
                .values_list(
                    "page__pk",
                    "page__name",
                    "page__url",
                    "column") \
                .order_by("column", "row")
               
        acl_d=vAcl().get_all_rights_by_user({"obj": True})
        users=User.objects.all() \
                .order_by("username") \
                .values_list("db", "username") \
                if request.sarvuser.pk \
                in PROJECT_ADMINS\
                else User.objects.filter(
                    db=request.sarvuser.db) \
                    .order_by("username") \
                    .values_list("db", "username")
        
        out={}
        for u in users:
            po_l=[]
            g = AclGroup()
            g.keyword = u[0] 
            groups = [g]
            c_n=p_l[0][3]
            n=0
            cn_d={}
            for p in p_l:
                if not p[2] \
                or not c_n == p[3]: #column header
                    cn_d.update({n:p[1]})
                    c_n=p[3]
                    continue
                elif p[2] is not None \
                and len(p[2]) > 0: 
                    o_d={}
                    for group in groups:
                        gkw=group.keyword
                        try: 
                            x = acl_d[u[1]][gkw][p[0]]
                        except KeyError: 
                            x = None
                        o_d.update({gkw:x})
                    po_l.append({p[1]:[p[0],o_d]})
                    n+=1
            out.update({u[1]: po_l})
        return out,[i[1] for i in users], cn_d
 
#Following rows to include link to admin splash page 
class AclCustom(admin.ModelAdmin):
    def has_add_permission(self,request):
        return False
    def has_change_permission(self,request):
        return False

