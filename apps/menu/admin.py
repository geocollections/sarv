# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse
import json

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from apps.acl.models import AclUserGroup,AclGroup,Acl as mAcl
from apps.acl.views import Acl

from sarv.utils import get_model
Menu, Page = get_model(["SarvMenu","SarvPage"])

institutions = ("git","elm","tug") 

class MenuAdmin(object):

    def is_active(self,request):
        #print (request.acl)
        pass
        
    def router(self, request, action=False):
        ''' Route url requests from urls.py to match views.py Acl class methods s'''
        response = False
        if hasattr(self, action):
            response = getattr(self, action)(request)
        else: print ('no attr')
        return HttpResponse(response)

    def indexsimple(self,request,only_list=False):
        pages_qs = Page.objects.filter(language=settings.LANGUAGE_CODE)
        pages = {item.pk:item for item in pages_qs}
        menu_qs = Menu.objects.filter(usergroup_id__isnull=True)\
                    .order_by('column','row','usergroup__pk')    
        z = {item.page_id:item for item in menu_qs}
        
        output={}
        i=0
        for k,item in pages.items():
            margs = {'id':z[k].id,'column':z[k].column,'row':z[k].row} if k in z \
                     else {'id':'p%s'%k,'column':0,'row':25+i}
            o = Menu(**margs)
            o.page_id = k
            o.active = 'Y' if k in z is not None else 'N'
            o.url = item.url
            o.name = item.name
            if not o.column in output: 
                output.update({o.column:{}})
            if o.row in output[o.column]:
                output[o.column].update({o.row:{}})
            output[o.column].update({o.row:o})
            i+=1 
        return render_to_response(
            "menu/menu-admin.html" if only_list is False else "menu/menu-admin_list.html",
            {'menu_list':output, 'institutions':institutions, 'num_columns':len(output)},
            RequestContext(request,{}),
        )
    
    def index(self,request):
        #kõik pages'd, mida kasutaja võib näha kui pole just adm
        #adm: kui lehe kasutajaõigused on adm
        selected_db = request.session['database']
        usergroup_id = AclUserGroup.objects\
            .get(user_id=request.session['sarvuser_id'],
                 group = AclGroup.objects.get(keyword=selected_db)
                 ).pk
        filter_args = {}
        request.acl[3] = True
        if not hasattr(request, 'acl') \
        or not request.acl[3] == True: #if is not admin, check acl
            #get_all_pages_where_user and db is
            ct = ContentType.objects.get_for_model("SarvPage")
            allowed_ids = mAcl.objects.filter(
                                         type='group',
                                         id_tested=usergroup_id,
                                         content_type=ct,
                                         rights_group_id__gt=1
                                         ).values_list('pk')
            filter_args.update({'pk__in':allowed_ids})
        filter_args.update({'language': settings.LANGUAGE_CODE})
        pages_qs = Page.objects.filter(**filter_args) # sic nested select < performances
        pages = {item.pk:item for item in pages_qs}
        menu_qs = Menu.objects.filter(Q(page_id__in=list(pages))\
                            & (Q(usergroup__pk=usergroup_id) | Q(usergroup__isnull=True))\
                            ).order_by('column','row','usergroup__pk')
        z = {}
        for item in menu_qs:
            if not item.page_id in z:
                z.update({item.page_id:{}})
            if not hasattr(z[item.page_id], 'usergroup') or\
                getattr(z[item.page_id],'usergroup') is None:
                z.update({item.page_id:item})
        output={}
        for k,item in pages.items():
            if k in z:
                o=Menu(id=k,column=z[k].column, row=z[k].row)
                o.active = 'Y' if z[k].usergroup_id is not None else 'N'
                o.url = item.url
                o.name = item.name
                if not o.column in output: output.update({o.column:{}})
                if o.row in output[o.column]:
                    output[o.column].update({o.row:{}})
                output[o.column].update({o.row:o})
        num_columns = len(output)
        
        return render_to_response(
            "menu/menu-admin.html",
            {'menu_list' : output, 'institutions':institutions, 'num_columns' : num_columns},
            RequestContext(request, {}),
        )

    def glist(self,request):
        return self.indexsimple(request, True)

    def set_column_order(self,request):
        self.is_active(request)
        if request.method == "GET":
            rows = request.GET.dict()
            rows = rows['sorted'].split('menucolumn[]=') #split to list
            rows.pop(0) #remove first that was empty
            rows = [r.replace('&', '') for r in rows] #remove '&'
            former = Menu.objects.filter(column__in=[p\
                     for p,v in enumerate(rows) if int(p) is not int(v)])\
                     .values_list('id','column').order_by('column')
            form_dict = {}
            for idi,col in former:
                if not col in form_dict: form_dict.update({col:[]})
                form_dict[col].append(idi)
            for p,v in enumerate(rows):
                if int(p) is not int(v) and int(v) in form_dict:
                    Menu.objects.filter(id__in=form_dict[int(v)]).update(column=p)
        response_data = {
            'reload':'glist',
            'destination':'.menu',
            'message':'Tulpade järjekord muudetud',
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
   
    def set_row_order(self,request):
        self.is_active(request)
        rows = request.GET.dict()
        
        column_update = int(rows['column_update'].replace('sortable-column-',''))
        rows = rows['sorted'].split('menuitem-')
        
        rows.pop(0)
        rows = [r.split('-') for r in rows]
        ids = [a for a,b in rows]

        for k,v in enumerate(ids):
            if v[:1] == 'p': 
                """ If page element hasn't yet been inserted into Menu """
                newitem = Menu(page_id=v[1:])
                newitem.save()
                v = newitem.pk
            Menu.objects.filter(id=v).update(column=column_update,row=k+1)
        b=[]
        for a in ids:
            b.append(a[1:] if a[:1] == 'p' else a)
        ids = b
        dupl_qs = Menu.objects.filter(column=column_update).exclude(id__in=ids)
        for i,item in enumerate(dupl_qs):
            Menu.objects.filter(id=item.pk,usergroup=None).exclude(row=0).update(row=k+i+1)
        
        response_data = {
            'reload':'glist',
            'destination':'.menu',
            'message':'Menüüpunkti asukoht muudetud',
        }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def set_status(self,request):
        self.is_active(request)
        data = request.GET.dict()
        
        if data['current_status'] == 'Y':
            Menu.objects.get(pk=int(data['id'])).delete()
        if data['current_status'] == 'N':
            kwargs = {
                'column':data['column'],
                'row':data['row'],
                'user_id':request.session['sarvuser_id'],
                'page_id':data['page_id'],
                'type':0,
                'active':'Y'
            }
            new_record = Menu(**kwargs)
            new_record.save()
        
        response_data = {
                'reload':'glist',
                'destination':'.menu',
                'message':'Status changed',
            }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def set_institution_status(self,request):
        self.is_active(request)
        input_data = request.GET.dict() #inst, id, current_status
        input_data.update({'destination':'main-menu','permission':1})
        if int(input_data['current_status']) == 1:
            del input_data['current_status']
            Acl().delete(input_data)
        else:
            del input_data['current_status']
            Acl().insert(input_data)
        response_data=False
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def set_row(self,request):
        self.is_active(request)
        
        input_data = request.GET.dict()
        response_data = {'message':'Error while inserting row'}
        if len(input_data) > 0:
            row = Page(name=input_data['name'], language=settings.LANGUAGE_CODE, visibility='acl')
            row.save()
            menu = Menu(column=1,row=Menu.objects.filter(column=1).count(),page_id=row.pk)
            menu.save()
            response_data = {
                'f':False,
                'reload':'glist',
                'destination':'.menu',
                'message':'Lehekülg lisatud.',
            }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def set_column(self,request):
        self.is_active(request)
        input_data = request.GET.dict()
        if len(input_data['name']) > 0:
            colname = Page(name=input_data['name'], language=settings.LANGUAGE_CODE, visibility='acl')
            colname.save()
            column = Menu(page=colname, row=0, column=Menu.objects.filter(row=0,usergroup_id__isnull=True).count()+1)#int(input_data['num_columns'])+1)
            column.save()
            response_data = {
                'f':False,
                'reload':'glist',
                'destination':'.menu',
                'message':'Tulp lisatud',
            }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")
          
    def delete_row(self,request):
        self.is_active(request)
        input_id = request.GET.dict()['id']
        page = Page.objects.filter(id=input_id)
        page.delete()
        response_data = {
            'reload':'glist',
            'destination':'.menu',
            'message':'Leheküljeviide kustutatud',
        }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def delete_column(self,request):
        self.is_active(request)
        rows = Menu.objects.filter(column=request.GET.dict()['column'])
        if len(rows) < 2:
            for item in rows:
                colname = Page.objects.filter(id=item.page_id)
                colname.delete()
            rows.delete()
            response_data = {
                'reload':'glist',
                'destination':'.menu',
                'message':'Menüü tulp kustutatud',
            }
        else:
            response_data = {'message':'First you have to delete column items.'}
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")

    def set_update_row(self,request):
        #self.is_active(request)
        input_data = request.GET.dict()
        Page.objects.filter(id=input_data['id']).update(name=input_data['name'],url=input_data['url'])
        response_data = {
            'reload':'glist',
            'destination':'.menu',
            'message':'Row data updated',
        }
        return HttpResponse(json.dumps(response_data), 
            content_type="application/json")
