# -*- coding: utf-8 -*-

import json
import os
import hashlib
import operator as join_operator
import mimetypes
import datetime
import types

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.serializers.json import DjangoJSONEncoder

from django.conf import settings

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from functools import reduce

from PIL import Image # Might not be in virtualenv. Needed by file uploader

from apps.nextify.config import (Page, Filter, MODELS_WITH_REMOTE_STORES)

from apps.nextify.utils import NextifyUtils
 
DEFAULT_FILES_DIR=""

def index (request, page="", action=None, element=None, **kwargs):
    
    if page == "":
        return HttpResponseRedirect("/")
    
    n = Nextify(request = request, 
                page = page, 
                action = action, 
                element = element)
    
    if not n.model:
        return HttpResponse(
            'Error. No model for this page')
    
    if not action \
    and not element:
        return render_to_response(
                'nextify/list.html', 
                n.get_filters(True))
    
    if ("-" in action 
        or n.utils.is_int(action)
        or action == 'add'):
        return n.get_form_page()
    
    if action == 'filters':
        return n.get_filters()
    
    if action == 'records':
        return n.get_records()
    
    if action == 'everything':
        return n.get_everything()
    
    if action == 'form_page_conf':
        return n.get_form_page_conf()
    
    if action == 'store':
        return n.get_store()
    
    if action == 'stores':
        return n.get_stores()
    
    if action == 'grids':
        return n.get_grids()
    
    if action == 'file':
        if not 'id' in kwargs:
            raise Http404
        return n.get_file(kwargs)
    
    if action == 'set_file':
        return n.set_file()
    
    if action == 'save':
        return n.set_record()
    
    if action == 'set_value':
        return n.set_value()
    
    if action == 'delete':
        return n.delete_record()
    
    if action == 'get_id_page':
        return n.get_id_page()
    
    if action == 'get_store_page_by_id':
        return n.get_store_page_by_id()

    if action == 'get_custom_filtersets':
        return n.get_custom_filtersets()
    
    if action == 'set_custom_filterset':
        return n.set_custom_filterset()
    
    if action == 'delete_custom_filterset':
        return n.delete_custom_filterset()
    
    # Sets that user has defined
    if action == 'get_custom_datasets':
        return n.get_custom_datasets()

    if action == 'get_in_custom_dataset':
        return n.get_in_custom_dataset()

    if action == 'set_custom_dataset':
        return n.set_custom_dataset()
    
    if action == 'set_custom_dataset_item':
        return n.set_custom_dataset_item()

    if action == 'delete_custom_dataset':
        return n.delete_custom_dataset()

class Nextify(object):
        
    def __init__(self, **kwargs):
        self.input = kwargs
        self.request = kwargs['request']
        self.c = getattr(Page, kwargs['page'])
        self.model = self.get_model()
        self.fields = None
        self.utils = NextifyUtils(self.input)
        self.utils.fields = {}
        self.utils.model = self.model
        self.utils.c = self.c

    def get_model (self, modelname=None):
        """
        Model instance
        
        @type modelname: string
        @param modelname: Django model class name
        """
        from sarv.utils import get_model
        
        n = self.c['model'] \
            if not modelname \
            else modelname
        m = get_model(n)
        s = self.request.session
        if 'database_id' in s \
        and isinstance(s['database_id'], int) \
        and hasattr(m, 'session_db'):
            m.session_db = s['database_id']
        return m

    def filters_l(self, g):
        """ 
        Add an item to default filters 
        
        @type g: dict
        @param g: {'default_filters','fname','fverbose_name','ftype'} 
        """
        if 'filters_default' \
        in self.c \
        and g['fname'] in \
        self.c['filters_default']:
            c=self.c['filters_default']
            out=[]
            f_d = getattr(Filter, g['ftype'])
            if isinstance(c[ g['fname'] ], int):
                k = c[ g['fname'] ]
                out=[g['fverbose_name'],
                     f_d.value_for_index(k),
                     g['ftype'], k]
            else:
                for i in c[g['fname']]:
                    v = f_d.value_for_index(i)
                    out=[g['fverbose_name'], 
                         v, g['ftype'], i]
            g['default_filters'].append(out)
        return g['default_filters']
    
    def get_filters (self, as_dict=None):
        """
        Gets filters for a page based on config
        values
        
        @type as_dict: boolean
        @param as_dict: Return results as dictionary
        
        """
        data={'name':self.input['page']}
        
        f_l=[] # list of filter parameters
        fd_l=[]
        fd_d={}
        try:
            c=self.c['filters_default']
            for i in c:
                for k,v in i.items():
                    fd_l.append(k)
                    fd_d.update({k:v})
        except:
            pass
        ft_d={}
        fv_d={}
        
        def get_filter_item(m, fc_n, v):
            """
            @param m: Django model
            @param fc_n: Filter fieldchain 
            """
            k=fc_n.split('__')
            vn_l=[]
            ft=False
            f_d={}
            for n,i in enumerate(k):
                try:
                    # Typical key
                    j=m._meta.get_field(i)
                    it=j.get_internal_type()
                    if it=='ForeignKey':
                        m=j.rel.to
                        #fk is last element in chain
                        if n+1==len(k):
                            fkf=m._meta.fields
                            
                            for fki in fkf:
                                #No deeper chains
                                if fki.get_internal_type() \
                                =='ForeignKey':
                                    continue
                                get_filter_item(self.model, 
                                    fc_n+'__'+fki.name, 0)
                                return
                    else:
                        ft=Filter.types[it]
                        f_d=getattr(Filter, ft)
                    vn_l.append(j.verbose_name)
                except:
                    # related_name
                    for i_ in m._meta.get_all_related_objects():
                        if i == i_.field.related_query_name():
                            m=i_.related_model
                            mn=m.__name__ \
                                if not hasattr(m, 'verbose_name') \
                                else m.verbose_name
                            vn_l.append(mn)
                            continue
            if not ft \
            or len(f_d) == 0:
                return     
            vn=':'.join(vn_l)
            
            vnt=(vn, ft)
            if not vnt in f_l:
                f_l.append(vnt)
            if not vn in fv_d:
                fv_d.update({vn: fc_n})
            if not vn in ft_d:
                ft_d.update({vn: ft})
            
            if fc_n in fd_l:
                v_=fd_d[fc_n]
                if isinstance(v_, int):
                    fd_d[fc_n]=[
                        vn,
                        f_d.value_for_index(v_),
                        ft,
                        v_
                    ]
            
                    
        for i in self.model._meta.fields:
            get_filter_item(self.model, i.name, 0)
        if 'filters_fk' in self.c:
            for i in self.c['filters_fk']:
                get_filter_item(self.model, i, 0)
        data.update({'fields': f_l,
                'fields_filter_types': ft_d,
                'fields_verbosenames': fv_d,
                'filters_types': self.utils.get_filters_list(),
                'filters_default': [fd_d[i] for i in fd_l],
                
                'settings':{},
                'singleton':True #needed Ext.define to function as repository of properties
        })
        
        ''' 
        2. GRID CONFIG 
        '''
        
        out = {'fields': [],
               'columns': [],
               'settings':{}}
                
        def col_title(g={'field':'', 'model':None}):
            m = g['model']
            vn = ''
            fl = g['field'].split('__')
            for n,j in enumerate(fl):
                try:
                    f = m._meta.get_field(j)
                except Exception as e:
                    print(e)
                    continue

                fvn = f.verbose_name \
                        if hasattr(f, 'verbose_name') \
                        else f.name
                vn += ': ' if len(vn) > 0 else ''
                vn += fvn
                if f.get_internal_type() != 'ForeignKey':
                    return vn
                elif len(fl) == n+1:
                    ''' 
                    If the last section is a foreign key, 
                    return the whole model list 
                    '''                          
                    return '%s: %s'%(vn, f.verbose_name)
                else:
                    try:
                        m = m._meta.get_field(j).rel.to
                    except:
                        print ('Field %s does not exist' % j)
                        break
        
        c = self.utils.c_io(self.c['fields'])
        
        idf=self.model._meta.pk.name

        f_l=[]
        for i in c['l']:
            f_l.append(i)
        #f_l=c['l']
        if 'pk' in c['l']:
            f_l.remove('pk')
        if 'id' in c['l']:
            f_l.remove('id')
        out['fields'] = ["in_custom_dataset",idf]+f_l
        
        '''
        get_everything adds data fields for form
        '''
        
        out['columns'].append({
            'dataIndex':'in_custom_dataset',
            'name':'in_custom_dataset',
            'sortable':False,
            'width':25,
			'xtype': 'sarv-booleancolumn',
        })        
        
        for fn in c['l']:
            t = col_title({'field': fn,
                           'model': self.model})
            
            col_d = {
                'dataIndex': fn,
                'text': t if t and len(t) > 0 else fn,
                'hidden': (True if fn in c['d'] \
                            and 'hidden' in \
                            c['d'][fn] else False)}
            col_c = c['d'][fn] if fn in c['d'] else None
            if col_c and len(col_c) > 0:
                col_d.update(col_c)
               
            out['columns'].append(col_d)
        
        out['settings'].update({
            'pageSize': self.c['pagesize'] \
                if 'pagesize' in self.c \
                else False
        })
        
        if 'grid_default' \
        in self.c:
            out['settings'].update({
                'doFilteredQuery':
                self.c['grid_default']})
        
        data.update({'records': out})
        
        w = self.c['form']['window']
        data.update({
            'popup': {'width': w['width'], 
                      'height': w['height']},
        })
        
        
        '''
        USER DATA
        '''
            
        ''' 
        ACL 
        '''
        try:
            from apps.acl.views import Acl as vAcl
            data.update({
                'acl': vAcl().get_page_user_rights(self.request)})
        except: 
            print ('No user rights specified!')
                
        '''
        OUTPUT GENERATION
        '''
        data=json.dumps(data,
                cls=DjangoJSONEncoder)
        
        if as_dict:
            return {'data':data}
        else:
            return HttpResponse(data, 
                content_type="application/json")
    
    def get_custom_filtersets (self):
        """
        @summary: Retrieves custom filtersets
        
        @rtype: HttpResponse
        """
        
        s = getattr(self.request, 'session')
        u_m = self.get_model('User')
        u = u_m.objects.get(pk=s['sarvuser_id'])
        
        m_n = 'SarvCustomDataset'
        cd_m = self.get_model(m_n)
        kw = {'params__startswith':'{"%s"' % 
                  self.input['page'],
                  'user__exact': u.username
        }
        qs = cd_m.objects.filter(**kw)
        
        d = [({'name': i.name, 
               'params': i.params
               })
             for i in qs]
        return HttpResponse(json.dumps({
                    'data': d,
                    'store_record_count': qs.count()
                }), 
                content_type="application/json")
    
    def set_custom_filterset (self):
        """
        @summary: Sets custom filterset
        """
        post = self.request.POST.dict()
        s = getattr(self.request, 'session')
        u_m = self.get_model('User')
        u = u_m.objects.get(pk=s['sarvuser_id'])
        
        m_n = 'SarvCustomDataset'
        cd_m = self.get_model(m_n)
        kw = {'name__exact': post['name'],
              'user__exact': u.username
        }
        out = {'success': True, 
               'error': False}
        
        qs = cd_m.objects.filter(**kw)
               
        if len(post['params'].replace(' ','')) == 0 \
        or len(post['name'].replace(' ','')) == 0:
            out['success'] = False
            out['error'] = True
            
        v = {'name': post['name'],
            'user': u.username,
            'params': json.dumps({
                    self.input['page']: 
                    post['params']}) 
        }
        
        if qs.count() > 0:
            try: 
                qs.update(**v)
            except:
                out.update({'success': False})
        else:
            n_m = self.get_model(m_n)
            n = n_m(**v)
            try:
                n.save()
                out.update({'id': n.id})
            except: 
                out.update({'success': False})
        return HttpResponse(json.dumps(out),
                    content_type="application/json")
    
    def delete_custom_filterset (self):
        """
        @summary: Deletes custom filterset.
        
        @rtype: HttpResponse
        """
        
        post = self.request.POST.dict()
        s = getattr(self.request, 'session')
        u_m = self.get_model('User')
        u = u_m.objects.get(pk=s['sarvuser_id'])
        
        m_n = 'SarvCustomDataset'
        cd_m = self.get_model(m_n)
        kw = {'name': post['name'],
              'user': u.username
        }
        qs = cd_m.objects.filter(**kw)
        out = {'success':True}
        try: 
            qs.delete()
        except: 
            out.update({'success':False})        
        return HttpResponse(json.dumps(out),
                    content_type="application/json")
    
    def get_custom_datasets(self):
        '''
        *Filtered based on given {modelname} (conf['model']?)
        1.List of dataset meta [id,remarks]
        2.Lists of dataset elements {id:[idel,idel2,idel3]}
        '''
        get=self.request.GET.dict()
        if 'k' in get:
            k=get['k']
            # Selection id is provided
            if self.utils.is_int(k):
                pass
            # Selection name is provided
            elif isinstance(k, str):
                pass
        m=self.get_model('SelectionSeries')
             
        qs=m.objects.filter(
            tablename=self.c['model'],
            user_added=self.request.sarvuser.username)
            # also database id?
        
        if 'query' in get \
        and len(get['query'].replace(' ','')) > 0:
            qs=qs.filter(remarks__istartswith=get['query'])
            
        start = int(get['start']) if 'start' in get else 0
        limit = int(get['limit']) if 'limit' in get else 50
        
        n = qs.count()
        qs = qs[start:(start+limit)] \
            .values_list('pk','remarks')
        
        r_l=[]
        for i in qs:
            r_l.append({'name':i[0],
                        'value':i[1] if i[1] \
                        else 'ID %i' % i[0]})
        return HttpResponse(
            json.dumps({'d': r_l, 'n': n }), 
            content_type="application/json")
    
    def get_in_custom_dataset(self):
        get=self.request.GET.dict()
        ids=get['in_custom_dataset']
        id_l=[]
        try:
            m=self.get_model('Selection')
            id_l=m.objects.filter(selection=int(ids)) \
                     .values_list('row', flat=True)
        except:
            pass
        if 'remote' in get:
            return HttpResponse(json.dumps({
				'id_l':list(id_l)}),
                    content_type="application/json")
        else:
            return id_l

    def set_custom_dataset(self):
        """
        Given data:
        1.Name/id of the dataset
        2.Members of the dataset
        If name is given, save it.
        """
        post=self.request.POST.dict()
        error=[]
        post.update({'no_bounds':True})
        __, qs_g, f_l, __ = self.get_records(True, post)

        qs_l=list(qs_g)
        if len(qs_l) == 0:
            error.append('no-records-found')
                
        if 'id' in f_l:
            pos=f_l.index('id')
        elif 'pk' in f_l:
            pos=f_l.index('pk')
        else:
            pos=None
        if self.utils.is_int(pos):
            id_l=[]
            for i in qs_l:
                id_l.append(i[pos])
        else:
            error.append('no-id-col')
        
        m=self.get_model('SelectionSeries')
        ms=self.get_model('Selection')
        if not 'k' in post:
            error.append('no-selection-identifier')
        if len(error) > 0:
            print(error)
            return HttpResponse('{}', 
                content_type="application/json")
        
        if not self.utils.is_int(post['k']):
            # Insert new selection type
            n_m=m.objects.filter(remarks=post['k']).count()
            if n_m > 0:
                post['k']=None
            from datetime import datetime
            new_i=m(tablename=self.c['model'],
                 user_added=self.request.sarvuser.username,
                 date_added=datetime.now() \
                    .strftime('%Y-%m-%d %H:%M:%S'),
                 remarks=post['k'])
            new_i.save()
            k=new_i
        else:
            k=m.objects.get(pk=post['k'])

        # Insert if not found
        q_l=ms.objects.filter(
            selection__pk=k.pk) \
            .values_list('row', flat=True)
        n_l=[]
        for i in id_l:
            if not i in q_l:
                n_l.append(
                    ms(row=i,
                      selection=k
                ))
        try:
            ms.objects.bulk_create(n_l)
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps({'id':k.pk}),
                    content_type="application/json")
    
    def set_custom_dataset_item (self):
        """
        @TODO: This method could be merged with 
        previous (set_custom_dataset) 
        @summary: Save a record to specified
        dataset. Used (primarily) to save 
        records one-by-one through list grid
        "+" button.
        @param post: {idr: <int: record id>, ids: <int: selectionseries id>}
        @type post: dict
        """
        post=self.request.POST.dict()
        error=[]
        if self.utils.is_int(post['ids']):
            m=self.get_model('SelectionSeries')
            s=m.objects.get(pk=int(post['ids']))
        else:
            error.append("incorrect-selection-id")
        if len(error) < 1 and s:
            ms=self.get_model('Selection')
            if self.utils.is_int(post['idr']):
                qs=ms.objects.filter(selection=s, row=int(post['idr']))
                if len(qs) < 1: 
                    ni=ms.objects.create(selection=s, row=int(post['idr']))
                else:
                    qs.delete()
            else:
                error.append("incorrect-record-id")
        else:
            error.append("no-selection-record")
        
        out = {'error':error} \
            if len(error) > 0 else \
            {'success': True}
        
        return HttpResponse(json.dumps(out),
                    content_type="application/json")

    def delete_custom_dataset(self):
        post=self.request.POST.dict()
        if not 'id' in post:
            return HttpResponse("", 
                content_type="application/json")
        
        ms=self.get_model('Selection')
        m=self.get_model('SelectionSeries')
        try:
            __ = ms.objects.filter(
                selection=post['id']).delete()
            __ = m.objects.get(
                    pk=post['id']).delete()
        except Exception as e:
            print(e)
        return HttpResponse('', 
            content_type="application/json")
    
    def get_columns (self, c, fk = False):
        """
        @summary: Get columns by config
        *config_list - particular page or 
        element list in page config list
        @param c: config
        @type c: dict 
        @param fk: 
        @type fk: str
         
        """
        if fk and fk in c: 
            c = c[fk]
        if not c \
        or not 'fields' in c:
            return
        if fk:
            m = self.model._meta \
                .get_field(
                    fk.replace('grid_','')).rel.to
        else:
            m = self.model \
                if not 'model' in c \
                else self.get_model(c['model'])
        
        if len(c['fields']) == 1:
            fields = self.utils.c_io(c['fields'][0])
        else:
            fields = self.utils.c_io(c['fields'])
            fields['l'] = []
            for field in m._meta.fields:
                try: 
                    fields['l'].append(field.name)
                except:
                    pass
        f_l=[]
        col_l=[]
        '''If there's Nextify dynamic page 
        defined in config, add button to grid'''
        if 'model' in c:
            url_to_form = [url for url in self.utils.get_url_list() \
                   if hasattr(Page, url) \
                   and 'model' in getattr(Page, url) \
                   and getattr(Page, url)['model'] == m.__name__ ] 
            if len(url_to_form) > 0:
                f_l.append({'name':'grid_urlbtn'})
                col_l.append({'dataIndex': 'grid_urlbtn',
                            'xtype': 'urlbtn',
                            'urlpart': url_to_form[0],
                            'sortable': False,})
        
        for fname in fields['l']:
            f_l.append({'name':fname})
            
            f_d = fields['d'][fname] \
                            if fname in fields['dict'] \
                            else {}
            f=m._meta.get_field_by_name(fname.split('__')[0])[0]

            col_d = {'dataIndex': fname,
                    'header': f.verbose_name \
                                if hasattr(f, 'verbose_name') \
                                else 'vname', 
                    'hidden': (True if 'hidden' in f_d else False),
                    'readOnly': (True if 'readonly' in f_d else False),
                    'xtype': m._meta.get_field(fname).get_internal_type() }
            if len(f_d) > 0:
                col_d.update(f_d)            
            col_l.append(col_d)
            
        return {
            'columns': col_l, 
            'fields': f_l
        }
    
    def get_records (self, as_dict=False, get=None):
        if not get:
            get = self.request.GET.dict()

        post = self.request.POST.dict()
        u = self.request.sarvuser
        out = {'fields': [],
               'columns': [],
               'records_total': 0,
               'settings': {'autoload': False}}

        if 'fp' in get \
        and len(get['fp']) > 0:
            fp_d = json.loads(get['fp'])
            fp_l=[]
            for a,b,c,d in fp_d['fp']:
                c = c
                if isinstance(d, str) \
                and len(d) > 0 \
                and d != " ":
                    fp_l.append([a,b,d])
        else:
            fp_l = []
        '''
        If 'grid_default' = 'my' in config, 
        load personal records, if 'all' in config, 
        load all records
        '''
        if 'grid_default' in self.c \
        and len(fp_l) < 1:
            out['settings'].update({
                'doFilteredQuery':
                self.c['grid_default']
            })

        q_l = [Q()]
        exclude_d = {}
        for f,op,val in fp_l:
            if not 'exclude_' in op \
            and val != "":     
                kw = { str('%s__%s' % (f, op)) : 
                      str(val)
                }
                q_l.append(Q(**kw));
            else:
                exclude_d['{0}__{1}'.format(f, op[8:])] = val
        
        '''
        Get custom dataset
        '''
        if 'custom_dataset_id' in get \
        and self.utils.is_int(get['custom_dataset_id']):
            c_id = get['custom_dataset_id']
            m = self.get_model('Selection')
            c_l = m.objects.filter(selection=c_id) \
                .values_list('row',flat=True)            
            f_l=[] 
            for i in c_l:
                f_l.append({'pk':{'exact':i}})
            q_l.append(self.utils.get_q_uery({'Or':f_l}))
            
        
        '''
        Get user records
        '''
        if 'myresults' in get \
        and get['myresults'] == 'yes' \
        and len(u.username) > 0:
            filter_d={'Or':[]}
            ufname=None
            try:
                self.model._meta.get_field_by_name('user_added')
                ufname='user_added'
            except: 
                try:
                    self.model._meta.get_field_by_name('user_created')
                    ufname='user_created'
                except: 
                    pass

            if ufname:
                filter_d = {'Or':[{ufname:{'exact':str(u.username)}}]}
                    
            if hasattr(self.model, 'owner'):
                filter_d['Or'].append({'owner':{'exact':u.pk}})
            
            q_l.append(self.utils.get_q_uery(filter_d))
            
            if not 'sort' in get \
            or ('sort' in get \
            and len(get['sort']) < 1):
                sortp=''
                try:
                    self.model._meta \
                        .get_field_by_name('timestamp')
                    sortp='timestamp'
                except:
                    try:
                        self.model._meta\
                            .get_field_by_name('date_changed')
                        sortp='date_changed'
                    except:
                        pass
                if len(sortp)>0:
                    get['sort']=json.dumps([{'property': sortp,
                                             'direction': 'DESC'}])
        ob_l = []
        if 'sort' in get:
            sort_z=json.loads(get['sort'])
            if not isinstance(sort_z, (dict, list)):
                sort_z=[sort_z]
            for row in sort_z:
                direction = '-' if 'direction' in row \
                                and row['direction'] == 'DESC' \
                                else ''  
                ob_l.append('{0}{1}'.format(direction, row['property']))
        
        start = int(get['start']) if 'start' in get else 0
        limit = int(get['limit']) if 'limit' in get else 50
        
        c = self.utils.c_io(self.c['fields'])
        f_l = c['l']
     
        ''' Make sure that 'pk' is first in the list '''
        if 'pk' in f_l:
            del f_l[f_l.index('pk')]
        if 'id' in f_l:
            del f_l[f_l.index('id')]
        pkn = self.model._meta.pk.name
        f_l.insert(0, pkn)
        
        '''Add compulsory fields if missing'''
        
        for i in ['user_added','user_changed']:
            if not i in f_l:
                f_l.append(i)
        
        '''
        get_everything adds data fields for form
        If remote store is included, then add form label field
        '''
        
        if as_dict:
            c_=self.utils.c_io(
                    self.utils.get_conf_model_mix(
                        self.c['form']['elements'], 
                        self.model))
            
            self.utils.get_stores_fields_list(self.c, False, self.model)
            
            for i in c_['l']:
                # If i field is remote store
                # fk value field should be inserted
                # besides id pointing to that fk object
                if (self.model.__name__ in self.utils.fk_d
                and i in self.utils.fk_d[self.model.__name__]):
                    fk_d=self.utils.get_store_model_fields(
                        self.model, i, c_['d'][i], settings.LANGUAGE_CODE)
                    if fk_d['m'].__name__ \
                    in MODELS_WITH_REMOTE_STORES:
                        rfn=i+'__'+fk_d['value_field']
                        if not rfn in f_l:
                            f_l.append(rfn)
                if not i in f_l \
                and not i.startswith('grid_') \
                and not i =='id': #'grid_' == i[:5] \
                    f_l.append(i)
            c_ = None
        try:
            self.model._meta \
                .get_field_by_name('owner')
            if not 'owner' in f_l:
                f_l.append('owner')
        except:
            pass
            
        '''
        Select related fields' list to optimize sql
        '''
        sr = []
        for i in f_l:                
            if '__' in i:
                rf_l = i.split('__')
                c_m = self.model
                for n,j in enumerate(rf_l):
                    rft = c_m._meta.get_field_by_name(j)
                    if rft == 'ForeignKey':
                        c_m = rft.rel.to
                        fk_n = rf_l[:n].join('__')
                        if not fk_n in sr:
                            sr.append(fk_n)
                    else:
                        break
                    
        '''
        Backwards relationships
        '''

        try:    
            qs = self.model.objects
            if len(sr) > 0:
                qs = qs.select_related(*sr)
            
            qs = qs.filter(reduce(join_operator.and_, q_l)) \
                .exclude(**exclude_d) \
                .values_list(*f_l)
            
            if len(ob_l) > 0: 
                qs = qs.order_by(*ob_l)
        except Exception as e:
            return None,[],[],{'error':str(e)}        
        
        try:
            qs_n = qs.count()
            
            if not 'no_bounds' in get \
            or not get['no_bounds']:
                qs = qs[start:(limit+start)]
            
            qs_g = qs.iterator() # NB! No cache 
        except Exception as e:
            print("[nextify.views #938] There's an error in database structure. SQL:")
            print("%s" % qs.query)
            return None,[],[],{'error':'Config field named \'%s\' not found in model %s' % 
                               (i,self.model.__name__)}
        
        #TODO: If foreignkey is date format, currently doesn't check it
        def qs_formatter(f_l, model):
            for i in qs_g: #qs_l:
                for n,j in enumerate(f_l):
                    fT = model._meta \
                            .get_field(j.split('__')[0]) \
                            .get_internal_type()
                    if fT in ('DateField','TimeField','DateTimeField'):
                        i=list(i)
                        i[n] = str(i[n]) if i[n] else None
                yield i
        
        '''
        Output
        '''
        if as_dict:
            del qs, out
            return qs_n, qs_formatter(f_l, self.model), f_l, {}
        # 8< -- 8<
        def col_title(given={'field':'', 'model':None}):
            m = given['model']
            vn = ''
            for n,j in enumerate(given['field'].split('__')):
                f = m._meta.get_field(j)
                fvn = f.verbose_name \
                        if hasattr(f, 'verbose_name') \
                        else f.name
                vn += ': ' if len(vn) > 0 else ''
                vn += fvn
                if f.get_internal_type() != 'ForeignKey':
                    return vn
                elif len(given['field'].split('__')) == n+1:
                    ''' 
                    If the last section is a foreign key, 
                    return the whole model list 
                    '''                          
                    return '%s: %s'%(vn, f.verbose_name)
                else:
                    try:
                        m = m._meta.get_field(j).rel.to
                    except:
                        print ('Field %s does not exist' % j)
                        break
        

        def get_col_title(c):
            for i in c['l']:
                t=col_title({'field':i,'model':self.model})
                col_d = {
                    'dataIndex': i,
                    'text': t if len(t) > 0 else i,
                    'hidden': (True if 'hidden' in c['d'][i] else False)}
                col_c = c['d'][i]
                if len(col_c) > 0:
                    col_d.update(col_c)
                yield {'name':i, 'columns': col_d}

        for cn in get_col_title(c):
            out['fields'].append({'name': cn['name']})
            out['columns'].append(cn['columns'])
        
        ''' Should go to config '''
        win_conf_d = self.c['form']['window']
        out['settings'].update({
            'popup': {'width': win_conf_d['width'], 
                      'height': win_conf_d['height']},
            'pagesize': self.c['pagesize'] \
                        if 'pagesize' in self.c \
                        else False
        })
    
        try:
            from apps.acl.views import Acl as vAcl
            out['settings'].update({
                'acl': vAcl().get_page_user_rights(self.request)})
        except: print ('No user rights specified!')
    
        if not 'type' in post:
            out.update({'records': [i for i in ds_formatter(f_l, self.model)]})

        return HttpResponse(json.dumps(out), 
                            content_type="application/json")
        # >8 -- >8
        
    def get_id_page(self, given = None):
        """
        'fp' - json
        'sort' - str || json
        'records_per_page' - int
        'input_id' - int
        """
        if not given:
            get = self.request.GET.dict()
        else:
            get = given
        if 'fp' in get and len(get['fp']) > 0:
            f_d = json.loads(get['fp'])
            fp_l=[]
            for a,b,c,d in f_d['fp']:
                c = c
                if len(d) > 0 and d != " ":
                    fp_l.append([a,b,d])
        else:
            fp_l = []
        
        f_l=[Q()]
        ex_d={}
        for fn,op,v in fp_l:
            if not 'exclude_' in op and v != "":     
                kw = {str('%s__%s' % (fn, op)) : str('%s' % v) }
                f_l.append(Q(**kw));
            else:
                ex_d['{0}__{1}'.format(fn, op[8:])]=v
        
        if 'myresults' in get \
        and get['myresults'] == 'yes' \
        and len(self.request.sarvuser.username) > 0:
            kw = { 'user_added__exact' : 
                str('%s' % self.request.sarvuser.username) }
            f_l.append(Q(**kw))
        
        ob_l=[]
        if 'sort' in get:
            if isinstance(get['sort'], str):
                d = '-' if 'direction' in get \
                    and get['direction'] is 'DESC' \
                    else ''
                ob_l.append('{0}{1}'.format(d, get['sort']))
            else: 
                sort_items = json.loads(get['sort'])
                for row in sort_items:
                    d = '-' if 'direction' in row \
                    and row['direction'] == 'DESC' \
                    else ''  
                    ob_l.append('{0}{1}'.format(d, 
                        row['property']))
        else:
            ob_l=[]
        
        '''Select related fields - to get queryset with the same size as query of records'''

        c = self.utils.c_io(self.c['fields'])
        t_l=[]
        for i in c['l']:
            e = i.split('__')
            del e[-1]
            if len(e) < 1:
                continue
            t_l.append('__'.join(e))

        m=self.model \
            if not given \
            or not 'model' in given \
            else given['model']
        
        qs=m.objects \
            .filter(reduce(join_operator.and_, f_l)) \
            .exclude(**ex_d)

        if len(ob_l) > 0:
            qs = qs.order_by(*ob_l)
        if len(t_l) > 0:
            qs = qs.select_related(*t_l)
        pos=-1
        t=m._meta.db_table
        
        sqlp=str(qs.query).split('FROM `%s`'%t)[1]
        
        if len(ob_l) < 1:
            sqlp=sqlp.split('ORDER BY')[0]

        sql = '''select x.position from (
                    select `%s`.id, @rownum:=@rownum+1 as position from `%s` 
                    join (select @rownum:=0) r
                    %s) x where x.id = %s ''' \
                    % (t, t, sqlp, get['input_id'])
        
        try:    
            sql_=sql.replace('LEFT OUTER JOIN', 'LEFT JOIN') \
                                .replace('INNER JOIN', 'LEFT JOIN') \
                                .replace('OUTER JOIN', 'LEFT JOIN')
            
            cursor = connections['sarv'].cursor()
            cursor.execute(sql_)
            pos=int(cursor.fetchone()[0])
        except Exception as e:
            print(e)
            print ('nextify: views.py: get_id_page(): failed to fetch record position from db')
        n = get['records_per_page']
        nr = 1
        if n > 0 and pos > -1:
            nr = (int(pos) - int(pos) % int(n))/int(n) + 1
            
            # When page number was in tens then 
            # calculated nr was wrong by one page
            # Therefore if pos ends with 0, divide 1
            if int(pos)%10 == 0:  

                nr-=1;
        if given:
            return int(nr)
        else:
            return HttpResponse(
                    json.dumps({'page_nr': int(nr)}),
                    content_type="application/json")

    '''
    get={'field','id',('limit'/'pageSize')}
    '''
    def get_store_page_by_id(self, given=False):
        
        get = given or self.request.GET.dict()
        
        c=self.utils.c_io(
            self.utils.get_conf_model_mix(
                self.c['form']['elements'], 
                self.model)
        )['d']
        f=get['field'] # get form field
        
        limit=int(get['limit']) \
                if 'limit' in get \
                else int(get['pageSize']) \
                if 'pageSize' in get \
                else 10
        fn_l=[]        
        if f.startswith('grid_') \
        and '__' in f:
            fn_l=f.split('__')
            c_=c[fn_l[0]]
            m=self.get_model(c_['model'])
            f=fn_l[1]
            size=c_['combobox_size'] \
                if 'combobox_size' \
                in c_ \
                else limit
        else:
            m=self.model
        
            size=self.c['form']['combobox_size'] \
                    if 'combobox_size' \
                    in self.c['form'] \
                    else limit
        
        fk_m=m._meta.get_field(f).rel.to
        
        if len(fn_l)==3:
            f=fn_l[2]
        
        if self.utils.is_int(get['id']):
            out=self.get_id_page({
                'input_id': get['id'],
                'records_per_page': size,
                'model': fk_m,
                'sort':f if not 'fk_field' in get \
                    else get['fk_field']
            })
        else:
            out=1
        
        if given:
            return out
        else:
            return HttpResponse(
                json.dumps(out),
                content_type="application/json")

    '''
    Get all data for selected list of records.
    Input: * sorting, offset, limiting from ExtJS; 
           * flag whether to include store data
    1. Based on given values get n records
    2. Get related grid data
    3. If stores flag, include store data
    '''
    def get_everything(self):
        out={'grids':{}}
        '''
        1. Records
        '''
        a = self.get_records(True)
        out.update({'records':{
            'n':a[0], 
			'd':a[1], 
			'f':a[2], 
			'msg':a[3]
		}})
                
        '''
        3. Custom Datasets
        '''
        ids_l=[]
        if 'in_custom_dataset' \
        in self.request.GET.dict():
            ids_l= self.get_in_custom_dataset()
        
        ids_ol=[]
        if 'id' in a[2]:
            cI=a[2].index('id')
        elif 'pk' in a[2]:
            cI=a[2].index('pk')
        
        def merge_custom_dataset_value():
            for i in a[1]:
                i.insert(0, True \
                    if i[cI] in ids_l \
                    else False)
                yield i
        
        out['records']['d'] = [list(i) for i in merge_custom_dataset_value()]
        
        out['records']['f'].insert(0, 'in_custom_dataset')


        '''
        2. Grids
        '''
        if 'id' in a[2]:
            cI=a[2].index('id')
        elif 'pk' in a[2]:
            cI=a[2].index('pk')
        out.update({'grids':
            self.get_grids((i[cI] for i in out['records']['d']))
        })

        return HttpResponse(json.dumps(out, 
                cls=DjangoJSONEncoder),
                content_type="application/json")


    def get_form_page_conf(self, as_dict = None):
        cf=[]
        strict = len(self.c['form']['elements'][0]) == 1 
        
        # Id to be the first field in form
        cf.append([['id',{
            'readOnly': True,
            'name':'id',    
        }]])
        
        if 'external_url' in self.c:
            cf[0].append(['_href',{
                'html':'<a href="" id="urlAnchor" data-url="'+self.c['external_url']+'"></a>',
                'padding':10,
                'border':0
            }])
        
        # force add compulsory fields
        # no need for get_form_model_mix
        f_l=self.utils.c_io(
                #self.c['form']['elements']
                self.utils.get_conf_model_mix(
                    self.c['form']['elements'], 
                    self.model)
            )['l']

        cf+=self.utils.get_conf_model_mix(
                    self.c['form']['elements'], 
                    self.model) 
                    
            
                        
        for i in ['user_added','user_changed']:
            if not i in f_l:
                cf.append([i,
                    {'hidden':True,
                     'name':i}])
        try:
            out={
                'formFields': [self.utils.reconf(i) \
                         for i in cf],
                'stores': self.get_stores(True),
                'user':{
                    'id': self.request.sarvuser.pk,
                    'name': self.request.sarvuser.username
                },
                'urls': self.get_urls(),
                'title': self.c['form']['title']
            }
        except Exception as e:
            out={"errors":[str(e)]}
        if as_dict:
            return out
        else:
            return HttpResponse(json.dumps(out, 
                    cls=DjangoJSONEncoder),
                    content_type="application/json") 

    def get_urls(self):
        # Get all dynamic pages
        u_l = self.utils.get_url_list()
        # siia peaks tulema - igale kombole href.
        # juhul kui leht on defineeritud
        # kombo peaks siis valima pigem mudeli nime kui kombo enda nime järgi
        
        out={}
        for u in u_l:
            if hasattr(Page, u) \
            and 'model' in getattr(Page, u):
                m=getattr(Page, u)['model'].lower()
                out.update({m:u})
        return out 
        
    def get_form_page(self):
        settings = {}
        errors = {}
        out = {'data':{}}
        
        is_local = False \
            if len(self.request.GET.dict()) > 0 \
            and 'o' in self.request.GET.dict() \
            else True
        
        has_id = True \
            if self.utils.is_int(self.input['action']) \
            else False
                    
        tpl = self.c['template'] \
                    if 'template' in self.c \
                    else 'form.html'

        store_size = (self.c['form']['combobox_size'] 
                         if 'combobox_size' in self.c['form'] \
                         else 10)
        record_id = self.input['action'] \
                            if self.utils.is_int(self.input['action']) \
                            else ''
        
        window = self.c['form']['window'] \
                            if 'window' in self.c['form'] \
                            else False
        settings.update({
                    'name':self.input['page'],
                    'popup':{ 'width': window['width'] \
                                            if 'width' in window \
                                            else '', 
                              'height': window['height'] \
                                            if 'height' in window \
                                            else '', },
                    'store_size': store_size,
                    'layout': self.c['form']['layout'] \
                                            if 'layout' in self.c['form'] \
                                            else ''
                    })

        out.update({
            'content': {
                'title': '',#title,
                'id': record_id
            },
            'settings': settings,
            'errors': errors
        })
        
        '''
        If page is static, 
        get all necessary data
        '''
        if is_local \
        and has_id:
            d={}
            d.update({
                'conf':out['settings']})

            '''
            Form page structure
            '''
            d['conf'].update(
                self.get_form_page_conf(True)
            )
            x=d['conf']['stores']
            del d['conf']['stores']
            d['conf'].update({
                'stores':{'data':x}}) 
            
            '''
            ACL
            '''
            try:
                from apps.acl.views import Acl as vAcl
                d['conf'].update({
                    'acl': vAcl().get_page_user_rights(
                                self.request)})
            except:
                print ('No user rights specified!')
            
            '''
            Form page data
            '''
            '''
            1. Records
            '''
            idr=self.input['action']
            get={'fp': json.dumps({'fp':[['pk', 'exact', 0, idr]]})}
            a = self.get_records(True, get)
            d.update({'records':{
                'n':a[0], 
                'd':[i for i in a[1]], 
                'f':a[2], 
                'msg':a[3]
            }})
            '''
            2. Grids
            '''
            if 'id' in a[2]:
                cI=a[2].index('id')
            elif 'pk' in a[2]:
                cI=a[2].index('pk')
            
            d['records'].update({'g': 
				self.get_grids((i[cI] for i in d['records']['d']))#r['d']))
            })
        
            out['data']=json.dumps(d, 
                cls=DjangoJSONEncoder)
        
        return render_to_response('nextify/%s' % tpl, out)

    def get_store(self, get_d=False):
        get = get_d or self.request.GET.dict()
        
        lang = settings.LANGUAGE_CODE
        f = get['field'] \
            if 'field' in get \
            else None
        if not f \
        or ('grid_' in f[:5] \
        and (not 'id' in get \
        or len(get['id']) < 1) \
        and not '__' in f): 
            return HttpResponse(json.dumps({}),
                    content_type="application/json")
                
        if not f:
            print ('[nextify.views.get_store] no store field specified')
            return HttpResponse(json.dumps({'store_records': False}),
                                content_type="application/json")
        
        '''
        3. Typical combobox store request
        '''
        ob_l=[]
        out={'store_records': [], 
             'store_record_count': 0}    

        start = int(get['start']) if 'start' in get else 0
        limit = int(get['limit']) if 'limit' in get else 10
        
        combo_size = self.c['form']['combobox_size'] \
                        if 'combobox_size' in self.c['form'] \
                        else limit
        
        e_d = self.utils.c_io(
                self.utils.get_conf_model_mix(
                    self.c['form']['elements'], 
                    self.model)
        )['d']
        
        if 'gridname' in get:
            if not get['gridname'] in e_d \
            or not 'model' in e_d[get['gridname']]:
                # VIGA
                pass
            m=self.get_model(e_d[get['gridname']]['model'])
            e_d=self.utils.c_io(e_d[get['gridname']]['fields'])['d']
        else:
            m=self.model
            
        fk_m = m._meta.get_field(f).rel.to
        if not get_d \
        and hasattr(fk_m, "session_db"):
            try:
                if "database_id" in self.request.session:
                    fk_m.session_db=self.request.session['database_id']
                else:
                    fk_m.session_db=None
            except:
                print("error views.py #1450")

        if not f in e_d \
        or not 'fk_label' in e_d[f]:
            print ('[nextify.views.get_store] combobox display field not defined \
                in config.py for "%s". Inserting first field after pk.' % f)
            rf_l = [item.name for item in fk_m._meta.fields]
            relf = rf_l[1 if rf_l[0] == 'id' else 0]
            
            e_d.update({f:{'fk_label':{lang:relf}}})
        
        fk_key_field = m._meta.get_field(f).rel.field_name
        fk_label_field = e_d[f]['fk_label'][lang]
        
        if 'id_to_page' in get \
        and self.utils.is_int(get['id_to_page']):
            
            p_nr=self.get_store_page_by_id({
                'field': f \
                    if not 'gridname' in get \
                    else get['gridname']+'__'+f+'__'+fk_label_field,
                'fk_field': fk_label_field,
                'id': get['id_to_page'],
                'limit': get['limit']
            })
            start=(p_nr-1)*limit
            out.update({'page':p_nr})
        
        ob_l.append(fk_label_field)
        
        fquery = None
        qarg = None
        sql = None
        if 'fk_filter' in e_d[f]:
            fk_filter = e_d[f]['fk_filter']
            if isinstance(fk_filter, str):
                if fk_filter[-1:] == '*':
                    fquery = 'icontains' \
                            if fk_filter[:1] == '*' \
                            else 'istartswith' 
                elif fk_filter[:1] == '*': 
                    fquery = 'iendswith'
            if isinstance(fk_filter, dict):
                if 'query' in get: 
                    del get['query']
                qarg = self.utils.get_q_uery(fk_filter)
            if isinstance(fk_filter, list) \
            and len(fk_filter) == 3 \
            and 'select' in (fk_filter[0][:6].lower()):
                if 'query' in get: 
                    del get['query']
                sql = fk_filter
        kw={} 
        if 'query' in get \
        and len(get['query']) > 0:
            kw.update({str('%s__istartswith' % fk_label_field):
                          str(get['query'])})
            start=0
        if fquery: 
            kw.update({str('%s__%s' % (fk_label_field, fquery)): 
                          e_d[f]['fk_filter'].replace('*','')})
        if len(kw) > 0:
            qs = fk_m.objects.filter(**kw)
        elif qarg:
            qs = fk_m.objects.filter(qarg)
        elif sql: 
            try:
                cursor = connections[sql[2] \
                            if not sql[2] in (False,None) \
                            else 'default'].cursor()
                cursor.execute(sql[0], sql[1] \
                            if isinstance(sql[1],(tuple,dict)) \
                            else None)
                raw_qs = cursor.fetchall()
                out['store_record_count'] = len(raw_qs)
            except:
                print ('[nextify.views.get_store] Error in raw SQL query') 
                qs = fk_m.objects.all()
                sql = False
        else: 
            qs = fk_m.objects.all()
        if get_d \
        and 'as_sql' in get_d:
            return qs.query()

        if len(ob_l) > 0:
            qs = qs.order_by(*ob_l)
        if not sql:
            out['store_record_count']=qs.count()
            qs_l=qs.values_list(
                fk_key_field, 
                fk_label_field
            )[start:(combo_size+start)]
            def qsttl():
                for i in qs_l:
                    yield list(i)
            out['store_records'] = [i for i in qsttl()]
        else: 
            out['store_records'] = [{'name':first,'value':second} \
                                    for first,second in raw_qs]
        if "database_id" in self.request.session \
        and hasattr(fk_m, "session_db"):
            fk_m.session_db=self.request.session['database_id']

        return HttpResponse(json.dumps(out),
                            content_type="application/json")
        
    
    def get_stores (self, as_dict=None):
        """ 
        Get all store data for a particular page
        
        @type as_dict: boolean
        @param as_dict: Response format
        """
        
        l=settings.LANGUAGE_CODE
        
        if not as_dict:
            get=self.request.GET.dict()
        else:
            get=[]

        c_i = self.utils.get_conf_model_mix(
            self.c['form']['elements'], 
            self.model
        ) 
        
        c_o = self.utils.c_io(c_i)
        c=c_o['d']
        
        def get_store_item (f,m,c_):
            fk_m = m._meta.get_field(f).rel.to
            if hasattr(fk_m, "session_db"):

                try:
                    if "database_id" in self.request.session:
                        fk_m.session_db=self.request.session['database_id']
                    else:
                        fk_m.session_db=None
                except:
                    print("error views.py #1590")
            out={'k':[],'d':[]}
            ff=self.utils.get_store_model_fields(m, f, c_, l)
            fk_name_field=ff['name_field']
            fk_value_field=ff['value_field']
            for k,v in ff['c_d'].items():
                c_.update({k:v})#=ff['c_d']
            
            fquery = None
            q_d = None
            sql = None
            if 'fk_filter' in c_:
                filt = c_['fk_filter']
                if isinstance(filt, str):
                    if filt[-1:] == '*':
                        fquery = 'icontains' \
                                if filt[:1] == '*' \
                                else 'istartswith' 
                    elif filt[:1] == '*': 
                        fquery = 'iendswith'
                if isinstance(filt, dict):
                    if 'query' in get: 
                        del get['query']
                    q_d = self.utils.get_q_uery(filt)
                    print(q_d)
                if isinstance(filt, list) \
                and len(filt) == 3 \
                and 'select' in (filt[0][:6].lower()):
                    if 'query' in get: 
                        del get['query']
                    sql = filt
            kw={} 
            if 'query' in get \
            and len(get['query']) > 0:
                kw.update({
                    str('%s__istartswith' % fk_value_field):
                    str(get['query'])
                })
            if fquery: 
                kw.update({
                    str('%s__%s' % (fk_value_field, fquery)): 
                    c_['fk_filter'].replace('*','')
                })
            if len(kw) > 0:
                fk_qs = fk_m.objects.filter(**kw)
            elif q_d: 
                fk_qs = fk_m.objects.filter(q_d)
            elif sql: 
                try:
                    cursor = connections[sql[2] \
                        if not sql[2] in (False, None) \
                        else 'default'].cursor()
                    cursor.execute(sql[0], sql[1] \
                        if isinstance(sql[1], (tuple,dict)) \
                        else None)
                    raw_qs = cursor.fetchall()
                    out['store_record_count'] = len(raw_qs)
                except:
                    print ('''[nextify.views.get_store] 
                        Error in raw SQL query''') 
                    fk_qs = fk_m.objects.all()
                    sql = False
            else: 
                fk_qs = fk_m.objects.all()
    
            out['k']=[fk_name_field,
                      fk_value_field]
            if not sql:
                qs = fk_qs.values(fk_name_field,
                            fk_value_field) \
                        .order_by(fk_value_field)
                
                out['d']=list([i[fk_name_field],i[fk_value_field]] for i in qs)
            else: 
                out['d']=list([i_n,i_v] \
                    for i_n,i_v in raw_qs)
            if "database_id" in self.request.session \
            and hasattr(fk_m, "session_db"):
                fk_m.session_db=self.request.session['database_id']
            return out
        
        out_={}
        for k in c_o['l']:
            if 'grid_'==k[:5]:
                gc={}
                for kk,vv in c_o['d'][k].items():
                    gc.update({kk:vv})
                mn=gc['model']
                rc=self.utils.c_io(
                    gc['fields'][0])
                ''' Iterate over grid items listed '''
                rm=self.get_model(mn)
                for i in rc['l']:
                    rf=rm._meta.get_field_by_name(i)[0]
                    if rf.get_internal_type() == 'ForeignKey' \
                    and not rf.rel.to.__name__ in \
                    MODELS_WITH_REMOTE_STORES:
                        rmc_d=self.utils.c_io(gc['fields'][0])['d']
                        c_d={} \
                            if not i in rmc_d \
                            else rmc_d[i]
                        stn=k+'__'+i
                        out_.update({
                            stn: get_store_item(i, rm, c_d)})
                        
            else:
                try:
                    f=self.model._meta.get_field_by_name(k)[0]
                    if f.get_internal_type() == 'ForeignKey' \
                    and not f.rel.to.__name__ in \
                    MODELS_WITH_REMOTE_STORES:
                        c_d={} \
                            if not k in c \
                            else c[k]
                        out_.update({
                            k: get_store_item(k, self.model, c_d) 
                        })
                except Exception as e:
                    print(e)
                    continue

        if not as_dict:
            return HttpResponse(
                    json.dumps(out_),
                    content_type="application/json"
            )
        else:
            return out_

    
    def get_grids (self, given=None):
        """
        Get all grid data for specified 
        page. Uses also paging
        """
        if not given:
            get=self.request.POST.dict()
            k_l=json.loads(get['k'])
        elif isinstance(given, types.GeneratorType):
            k_l=list(given)
        else:
            k_l=given # should be {k:[<id1>,..]}
        c = self.utils.c_io(
                self.utils.get_conf_model_mix(
                    self.c['form']['elements'], 
                    self.model)
            )['d']
        errors=[]        
        relqs={}
        for k,v in c.items():
            if 'grid_' == k[:5]:
                m=self.get_model(v['model'])
                f_c=self.utils.c_io(v['fields'][0])
                pkfn=m._meta.pk.name #pk field name
                n_l=[v['related_field'], pkfn]+f_c['l']
                ''' Add remote combo label fields to the mix '''
                
                for i in f_c['l']: #[1:]:
                    # If i field is remote store
                    # fk value field should be inserted
                    # besides id pointing to that fk object
                    try:
                        m._meta.get_field(i)
                    except Exception as e:
                        errors.append(str(e))
                        continue
                    if m._meta.get_field(i) \
                    .get_internal_type() == \
                    'ForeignKey':
                        cc_d={} \
                            if not i in f_c['d'] \
                            else f_c['d'][i] 
                        fk_d=self.utils.get_store_model_fields(
                            m, i, cc_d, settings.LANGUAGE_CODE)
                        
                        if fk_d \
                        and fk_d['m'].__name__ \
                        in MODELS_WITH_REMOTE_STORES:
                            rfn=i+'__'+fk_d['value_field']
                            if not rfn in n_l:
                                n_l.append(rfn)

                try:
                    rqs=m.objects.filter(\
                        **{v['related_field']+'__in':k_l}) \
                            .values_list(*n_l)
                except Exception as e:
                    errors.append(str(e))
                    continue
                
                try:
                    for i in rqs:
                        pass
                except Exception as e:
                    errors.append(str(e))
                    continue
              
                '''
                Extra formatting for Ext
                '''               
                f=[]
                fc=[]
                for j in n_l[2:]:
                    f.append('id_' \
                        if j == 'id' \
                        else j)
                    try:
                        if not '__' in j:
                            fit=m._meta.get_field(j) \
                                .get_internal_type()
                        else:
                            fk_f=j.split('__')
                            
                            fk_m=m._meta.get_field(fk_f[0]).rel.to
                            fit=fk_m._meta.get_field(fk_f[1]) \
                                .get_internal_type()

                    except Exception as e:
                        print(e)
                    r={'name':'id_' \
                             if j == 'id' \
                             else j,
                        'type': 'int' \
                            if fit in ('IntegerField') \
                            else 'float' \
                            if fit == 'FloatField' \
                            else 'boolean' \
                            if fit == 'BooleanField' \
                            else 'string'}
                    if fit=='ForeignKey':
                        del r['type']
                    if 'type' in r \
                    and r['type'] in ('int','float'):
                        r.update({'useNull':True})
                    fc.append(r)
                
                if not k in relqs:
                    #m-map,r-records,f-fields
                    relqs.update({k:
                        {'r':{}, 'm':{}, 'f':f, 'fc':fc}})
                
                for i in rqs:
                    for j in i:
                        if not j:
                            j=''
                    rf = i[0]
                    if not rf in relqs[k]['m']:
                        relqs[k]['m'].update({rf:[]})
                    if not i[1] in relqs[k]['r']:
                        relqs[k]['r'].update(
                            {i[1]:i[2:]})
                    relqs[k]['m'][rf].append(i[1])
        
        if len(errors) > 0:
            print(errors)
            if not 'msg' in relqs:
                relqs.update({'msg':{}})
            if not 'error' in relqs['msg']:
                relqs['msg'].update({'error':[]})
            relqs['msg']['error']=errors

        if not given:
            return HttpResponse(json.dumps(relqs, 
                        cls=DjangoJSONEncoder),
                    content_type="application/json")
        else:
            return relqs
    
    def get_file(self, given):
        
        if not ('id' in given \
        and 'id' in given):
            raise Http404
        
        r=self.request
        c={}
        c_d = self.utils.c_io(
            self.utils.get_conf_model_mix(
                self.c['form']['elements'],
                self.model)
        )['d']

        for v in c_d.values():
            if 'file' in v:
                for k,v in v['file'].items():
                    c.update({k:v})
        if not 'path' in c:
            c.update({'path': 
                DEFAULT_FILES_DIR})
        c['path']=c['path'].rstrip('/')
        
        fhn=self.get_file_hash('', given['id'])
        
        subdir=fhn[0:2]
        filen=''
        p_to=c['path']+'/'+subdir
        # Find file with such hash
        if not os.path.exists(p_to):
            raise Http404
        for file in os.listdir(p_to):
            if file.startswith(fhn):
                filen=file
        if not filen:
            raise Http404
                
        if not hasattr(settings, 'NEXTIFY_DOWNLOAD_DIR'):
            print('No download folder defined in local_settings. Use name NEXTIFY_DOWNLOAD_DIR')
            raise Http404
            
        fpath=os.path.join(
            settings.NEXTIFY_DOWNLOAD_DIR, 
            fhn[0:2], filen)
        
        try:
            fp = open(fpath, 'rb')
        except FileNotFoundError:
            raise Http404
        
        resp = HttpResponse(fp.read())
        fp.close()
        ftype, enc= mimetypes.guess_type(filen)
        if ftype is None:
            ftype = 'application/octet-stream'
        resp['Content-Type'] = ftype
        resp['Content-Length'] = str(os.stat(fpath).st_size)
        if enc is not None:
            resp['Content-Encoding'] = enc
        
        # To inspect details for the below code, 
        # see http://greenbytes.de/tech/tc2231/
        if u'WebKit' in r.META['HTTP_USER_AGENT']:
            # Safari 3.0 and Chrome 2.0 accepts 
            # UTF-8 encoded string directly.
            fheader = 'filename=%s' % filen.encode('utf-8')
        elif u'MSIE' in r.META['HTTP_USER_AGENT']:
            # IE does not support 
            # internationalized filename at all.
            # It can only recognize internationalized URL, 
            # so we do the trick via routing rules.
            fheader = ''
        else:
            import urllib
            # For others like Firefox, we follow RFC2231 
            # (encoding extension in HTTP headers).
            fheader = 'filename*=UTF-8\'\'%s' % \
                urllib.parse.quote(filen.encode('utf-8'))
        resp['Content-Disposition'] = 'attachment; ' + fheader
        return resp    
        
    def mkdir(self, path):
        #start from the beginning
        p='/'
        p_l=path.split('/')
        for i in p_l:
            if len(i)==0:
                continue
            try:
                if not os.path.exists(p+i):
                    os.mkdir(os.path.join(p, i))    
            except Exception as e:
                print("[nextify.views.mkdir] %s"%e)
            p+=i+'/'
        return p
    
    def save_file(self, f, c):
        if not 'hash' in c \
        or not isinstance(c['hash'], str):
            return
            
        self.mkdir(c['path'])
        
        #remove files with same names (for example )
        try:
            h=c['hash'].split('.')[0]
            for file in os.listdir(c['path']):
                if file.startswith(h):
                    os.remove(c['path']+'/'+file)
        except Exception as e:
            print(e)
        
        #save file
        try:      
            c['path']+='/'+c['hash']
            destination = open(c['path'], 
                'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
        except Exception as e:
            print(e)
        return c['path']
    
    def get_filename_ext(self, path):
        """
        
        """
        path=path.lower()
        for ext in ['.tar.gz', '.tar.bz2']:
            if path.endswith(ext):
                return path[:-len(ext)], path[-len(ext):]
        return os.path.splitext(path)
    
    def get_file_hash(self, ext, idr):
        """
        @
        given - 
        """
        md=hashlib.md5()

        t='attachment.'+str(idr)
        md.update(t.encode('utf-8'))

        return md.hexdigest()+ext
    
    def resize_image(self, c, p_from, p_to, fname):
        """
        @param 
        """
        i_o=Image
        f=i_o.open(p_from)
        e=[]
        try:
            rf=f.resize((
                c['width'], 
                c['height']), 
                i_o.ANTIALIAS)
        except Exception as err:
            e.append(err)
        rfname=p_to+'/'+fname
        try:
            self.mkdir(p_to)
            # Delete all files that have 
            #same hash but different extension
            h=fname.split('.')[0]
            for file in os.listdir(p_to):
                if file.startswith(h):
                    os.remove(p_to+'/'+file)
            rf.save(rfname)
        except Exception as err:
            e.append(err)
        return err, rfname
    
    def set_file(self, given=None):
        # given={'id'-record id, 'fieldname'?}
        e=[]
        
        if not given:
            given = self.request.POST.dict()
        
        #get field conf
        c_d = self.utils.c_io(
            #self.c['form']['elements']
            self.utils.get_conf_model_mix(
                self.c['form']['elements'], 
                self.model)
        )['d']
        
        c={}
        if 'fieldname' in given \
        and given['fieldname']+'-file' \
        in self.request.FILES \
        and 'id' in given:
            x=c_d[given['fieldname']]['file'] \
                if given['fieldname'] in c_d \
                and 'file' in c_d[given['fieldname']] \
                else {}
            
            for k,v in x.items():
                c.update({k:v})
            c.update({
                'path': c.get('path', DEFAULT_FILES_DIR)
            })
            
            f=self.request.FILES[given['fieldname']+'-file']
            ext=self.get_filename_ext(f.name)[1]
            
            c.update({
                'hash': self.get_file_hash(
                            ext, given['id'])
            })
            
            c['path']=c['path'].rstrip('/')
            
            subdir=''
            if 'dir_depth' in c:
                # If depth is greater than 
                # the length of hash, set
                # length to equal hash length
                if len(c['hash']) < c['dir_depth']:
                    c['dir_depth']=len(c['hash'])
                
                for i in range(c['dir_depth']):
                    subdir+='/'+c['hash'][i*2:2+(i*2)]

            c['path']+=subdir
            try:
                npath=self.save_file(f, c)
            except Exception as er:
                e.append(er)
            
            #create thumbnail preview for images
            
            c_=c.get('preview', {})
            
            if ext.lower() \
            in ['.jpg','.png','.gif'] \
            and 'max_size' in c_ \
            and 'path' in c_:
                             
                ni=Image
                f_=ni.open(npath)
                
                (width,height) = f_.size
                if width > height:
                    size_= c_['max_size'], \
                            height/width*c_['max_size']
                else:
                    size_= width/height*c_['max_size'], \
                            c_['max_size']
                import math
                size_=math.floor(size_[0]), \
                        math.floor(size_[1])
                
                try:
                    
                    rf=f_.resize(
                        size_,
                        ni.ANTIALIAS
                    )
                except Exception as err:
                    e.append(err)    
                c_['path']=c_['path'].rstrip('/')
                rfname=c_['path']+subdir+'/'+c['hash']
                
                try:
                    self.mkdir(c_['path']+subdir)
                    
                    # Delete all files that have same hash but different
                    # extension
                    h=c['hash'].split('.')[0]
                    for file in os.listdir(c_['path']+subdir):
                        if file.startswith(h):
                            os.remove(c_['path']+subdir+'/'+file)
                    
                    rf.save(rfname)
                except Exception as err:
                    e.append(err)
            if len(e)==0:
                if not 'fieldname_hashed' in c:
                    print('Dd file upload. Updating database. No fieldname_hashed specified in config')
                try:
                    to_db_d={
                            given['fieldname']: f.name,
                            c['fieldname_hashed']: c['hash'],
                            'user_changed':'',
                            'date_changed':''
                    }
                    
                    u = self.request.sarvuser.username
                    from datetime import datetime
                    try:
                        self.model._meta.get_field_by_name('user_changed')
                        to_db_d.update({
                            'user_changed': u,
                            'date_changed': datetime.now()})
                    except: 
                        pass
                    
                    self.model \
                        .objects \
                        .filter(pk=int(given['id'])) \
                        .update(**to_db_d)
                except Exception as err:
                    e.append(err)
        
        # If there were errors, 
        # remove freshly uploaded
        # file and its preview
        if len(e) > 0:
            if os.path.exists(npath):
                os.remove(npath)
            if os.path.exists(rfname):
                os.remove(rfname)
        out={
            'errors': [str(i) for i in e],
            'data':{
                'hash': c['hash']
            }
        }
        del(c)
        return HttpResponse(json.dumps(out), 
                    content_type="application/json")
    
    def set_record(self):
        post = self.request.POST.dict()
        conf = self.utils.c_io(
            self.utils.get_conf_model_mix(
                self.c['form']['elements'], 
                self.model)
        )
        r = {'errors':[]}
        items_to_db = {}
        
        if 'get_page_by_id' in post \
        and post['get_page_by_id']:
            try:
                find=json.loads(post['get_page_by_id'])
            except:
                pass
            del post['get_page_by_id']
        else:
            find=False
        
        '''
        Subgrid save 
        '''
        grid_cdf_d={}
        if 'gridname' in post:
            conf = conf['d'][post['gridname']]
            if not 'id' in post:
                post['saveAs'] = True
            if not 'model' in conf \
            or (not 'grid_parent_id' in post \
            and not 'id' in post): 
                return HttpResponse(json.dumps({}),
                                    content_type="application/json")
            self.model = self.get_model(conf['model'])
            
            
            cdf_di={}
            if '_combo_labelfield_l' in post:
                cdf_l=post['_combo_labelfield_l'].split(',')            
                for cdf in cdf_l:
                    cdf_f=cdf.split('__')
                    if len(cdf_f) > 1:
                        cdf_di.update({cdf_f[0]:cdf_f[1]})

            #save
            if not 'id' in post \
            or not self.utils.is_int(int(post['id'])):
                print("saving grid")
                for f in self.model._meta.fields:
                    if f.get_internal_type() == 'ForeignKey':
                        idr=False
                        fk_obj = self.model._meta \
                                    .get_field(f.name).rel.to
                        idr=int(post['grid_parent_id']) \
                            if fk_obj.__name__==self.c['model'] \
                            else int(post[f.name]) \
                            if f.name in post \
                            and len(post[f.name]) > 0 \
                            else False
                        if not idr:
                            continue
                        try:
                            if hasattr(fk_obj, "session_db"):
                                sdb=fk_obj.session_db
                                fk_obj.session_db=None
                            new_fk_obj = fk_obj.objects.get(pk=idr)
                            post[f.name]=new_fk_obj
                            if hasattr(fk_obj, "session_db"):
                                fk_obj.session_db=sdb
                            # Grid Remote combos have value fields which need to be populated
                            if f.name in cdf_di:
                                if hasattr(new_fk_obj, cdf_di[f.name]):
                                    grid_cdf_d.update({f.name+"__"+cdf_di[f.name]:
										str(getattr(new_fk_obj, cdf_di[f.name]))})

                        except ObjectDoesNotExist:
                            continue
                        except Exception as err:
                            r['errors'].append(str(err))
            else:
                # on update:
                # If id then grid record
                # is updated: don't need
                # to find parent record's
                # object
                for f in self.model._meta.fields:
                    if f.get_internal_type() == 'ForeignKey':
                        fk_o=self.model._meta.get_field(f.name).rel.to
                        if hasattr(fk_o, '__name__') \
                        and fk_o.__name__ == self.c['model']:
                            #Is marked as related field
                            if 'related_field' in conf \
                            and f.name==conf['related_field']:
                                try:
                                    post[f.name]=int(post['grid_parent_id'])
                                except ObjectDoesNotExist:
                                    continue
                print('upd')
                print(post)
            if 'grid_parent_id' in post:
                del post['grid_parent_id']
            del post['gridname']
        
        '''
        Form save
        '''
        if 'id_hidden' in post: 
            del post['id_hidden'] 
        if 'parent_url_val' in post: 
            del post['parent_url_val']
        
        tobedeleted=[]
        for k in post.keys():
            if k.startswith('grid_'): 
                tobedeleted.append(k) # 'grid_drillcore' <= get from model all associations and save rel after save
        for i in tobedeleted: 
            del post[i]
        
        save_as = True \
            if 'saveAs' in post \
            else False
        if save_as: 
            del post['saveAs']
        
        fk_unset = []

        m=self.model
        mf=m._meta.fields
        cdf_d={}
        for f in mf:
            k = f.name
            v = post.get(f.name)
            ft = f.get_internal_type()
            if not k in post:
                continue
            if ft == 'ForeignKey':
                if v in ['','None',None]:
                    fk_unset.append(f.name)
                    post[f.name] = None
                    continue
                elif self.utils.is_int(v):
                    fk_m = f.rel.to
                    pk = fk_m._meta.pk.name
                    try:
                        qs = fk_m.objects.get(**{pk:v})
                    except fk_m.DoesNotExist as err1:
                        print("does not exist")
                    except Exception as err:
                        r['errors'].append(str(err))
                    try:
                        if qs:
                            v = qs
                    except:
                        pass
                ''' '''            
            elif f.name in ['id','pk'] \
            and (save_as \
            or (not save_as and len(v) < 1)):
                continue
            if ft in ('IntegerField') \
            and v == '': 
                v = None
            if ft in ('BooleanField','NullBooleanField'): #should optimize - remove " from extjs input
                if v in ('True','true',1): 
                    v = True
                elif v in (False,'False','false',0): 
                    v = False
                elif v in ('None','none','Null','',): 
                    v = None
            if ft in ('ForeignKeyField') \
            and isinstance(v, str) \
            and len(v) > 0 \
            and (not 'id' in post \
            or len(post['id']) == 0 \
            or (not save_as \
            and 'id' in post \
            and self.utils.is_int(post['id']))):# added update for grid combos that might be given as values
                fk_obj = self.model._meta.get_field(f.name).rel.to
                r['errors'].append("Copy this error message: "+fk_obj.query)
                if self.utils.is_int(v):
                    #try:
                    v = fk_obj.objects.get(pk=int(v))
                    #except fk_obj.DoesNotExist:
                    r['errors'].append("Copy this error message: "+v.query)
                else:
                    print ('#930: no int given')
            if f.unique \
            and 0 < m.objects.filter(**{k:v}).count() < 2:
                # If there's a readonly field that's unique, 
                # skip it but don't give an error 
                if (k in conf \
                and 'readonly' in conf[k]) \
                or (not save_as \
                and 'id' in post \
                and self.utils.is_int(post['id'])) \
                or (save_as and f.name == 'id'): 
                    continue
                else: 
                    r['errors'].append('Väärtus %s on andmebaasis juba olemas' % v)
            if post[k] in (None,''): 
                fk_unset.append(k)
            elif post[k]:
                items_to_db[k] = v
        
        # database_id
        if 'database' in \
        [i.name for i in \
        m._meta.fields] \
        and not 'database' \
        in items_to_db:
            s=self.request.session
            if 'database_id' in s:
                #from apps.nextify.models import Database
                from sarv.utils import get_model
                Database = get_model("Database")
                dbi=Database.objects.get(pk=s['database_id'])
                items_to_db.update({
                    'database': dbi})
        
        if 'combo_defaults' in post: 
            del post['combo_defaults'] 
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        u = self.request.sarvuser
        if len(r['errors']) < 1:
            try: 
                m._meta.get_field_by_name('user_changed')
                items_to_db.update({'user_changed':u.username,
                                'date_changed':timestamp})
            except: pass    
            try: 
                m._meta.get_field_by_name('user_created')
                if not 'user_created' in items_to_db\
                or items_to_db['user_created'] in ('',None):
                    items_to_db.update({'user_created':u})
                items_to_db.update({'timestamp_created':timestamp})
            except: pass
            try:
                m._meta.get_field_by_name('user_modified')
                if not 'user_modified' in items_to_db\
                or items_to_db['user_modified'] in ('',None):
                    items_to_db.update({'user_modified':u})
                items_to_db.update({'timestamp_modified':timestamp})
            except: pass
            
            for item in ['user_changed','date_changed','user_created','user_modified']:
                if item in fk_unset: 
                    fk_unset.remove(item)
        if not save_as \
        and 'id' in post \
        and self.utils.is_int(post['id']):
            #'updating..'
            r['isUpdate']=True
            current_model = m.objects.filter(pk=post['id'])
            if len(fk_unset) > 0:
                for k in fk_unset:
                    items_to_db.update({k:None})
            try:
                current_model.update(**items_to_db)
                r['id'] = post['id']
            except TypeError as e:
                r['errors'].append(e);
            except Exception as e:
                r['errors'].append('Viga kirje andmete uuendamisel:%s'%e)
        else:
            #'saving..'
            current_id=post['id'] if 'id' in post else None
            
            if 'id' in items_to_db:
                current_id=items_to_db['id'] 
                del items_to_db['id']
            try: 
                m._meta.get_field_by_name('user_added')
                items_to_db.update({'user_added':u.username,
                                    'date_added':timestamp})
            except: pass
            try:
                m._meta.get_field_by_name('user_created')
                items_to_db.update({'user_created':u.username,
                                    'timestamp_created':timestamp})
            except: pass
            try:
                new_item = self.model(**items_to_db)
            except Exception as e:
                r['errors'].append('Viga kirje salvestamisel:%s'%e)
            if len(r['errors']) < 1:
                try:
                    ''' Actual db query '''
                    new_item.save()
                    
                    ''' Add related objects '''
                    if 'd' in conf:
                        import copy
                        for kx,vx in conf['d'].items():
                            if kx.startswith('grid_') \
                            and 'duplicable' in vx \
                            and vx['duplicable']:
                                if not 'model' in vx \
                                or not 'related_field' in vx:
                                    print("Config %s missing model and/or related_field params" % kx)
                                    continue
                                mx=self.utils.get_model(vx['model'])
                                if not self.utils.is_int(current_id):
                                    continue
                                qsx=mx.objects.filter(**{vx['related_field']: current_id})
                                no_i=[]
                                for o in qsx:
                                    nc=copy.copy(o)
                                    if hasattr(nc, "id"):
                                        setattr(nc,"id", None)
                                    if hasattr(nc, "pk"):
                                        setattr(nc, "pk", None)
                                    setattr(nc, vx['related_field'], new_item)
                                    no_i.append(nc)
                                if(len(no_i) > 0):
                                    mx.objects.bulk_create(no_i)
                    r.update({'id':new_item.id})
                    
                    ''' 
                    Could look up correct page on one go
                    '''
                    if find:
                        find.update({
                            'input_id': r['id']})
                        try:
                            if 'fp' in find:
                                fp=json.dumps({'fp':find['fp']})
                                find.update({'fp':fp})
                            
                            if 'sort' in find \
                            and isinstance(find['sort'], str) \
                            and len(find['sort']) < 1:
                                find['sort']="id"
                                #del find['sort']
                            p_nr = self.get_id_page(find)
                        except Exception as e:
                            print(e)
                            p_nr = False
                        if p_nr:
                            r.update({
                                'page':p_nr})
                except Exception as e:
                    print(e)
                    r['errors'].append('Viga kirje andmebaasi lisamisel:%s' % e);
        r.update({
            'success': True \
                if len(r['errors']) < 1 \
                else False})
        r.update({'data':{}})
        for k,v in items_to_db.items():
            v_=None
            if isinstance(v, (str,int)):
                v_=v
            elif not v:
                pass
            else:
                v_=v.pk
            r['data'].update({k:v_})
        
        for k,v in grid_cdf_d.items():
            r['data'].update({k:v})
        return HttpResponse(json.dumps(r),
                            content_type="application/json")
    
    def set_value (self):
        post = self.request.POST.dict()
        
        c = self.utils.c_io(
                self.utils.get_conf_model_mix(
                self.c['form']['elements'],
                self.model)
            )['d'][post['grid']]
        if not 'model' in c: 
            return HttpResponse('{}',
                content_type="application/json")
        
        k = post['name']
        v = post['value']
        r = {'errors':[]}
        lang = settings.LANGUAGE_CODE
        m = self.get_model(c['model'])
        to_db_d = {}
        
        if not k == 'id': 
            ft = m._meta.get_field(k) \
                            .get_internal_type()     
            if ft in ('IntegerField') \
            and v == '': 
                v = None
            #should optimize - remove " from extjs input
            if ft in ('BooleanField', 'NullBooleanField'):
                if v in ('True', 'true', 1): 
                    v = True
                elif v in (False, 'False', 'false', 0): 
                    v = False
                elif v in ('None', 'none', 'Null', ''): 
                    v = None
            if ft in 'ForeignKey':
                fk_m = m._meta.get_field(k).rel.to    
                if not self.utils.is_int(v):
                    el = self.utils.c_io(c['fields'])['d']
                    if not k in el \
                    or not 'fk_label' in el[k]:
                        print ('[nextify.views.set_value] combobox display field not defined in config.py for "%s"' % k)
                        el.update({k:{
                            'fk_label':{
                                lang:[i.name for i in \
                                    fk_m._meta.fields][0]
                        }}})
                    fk_crit = {el[k]['fk_label'][lang]: v}
                else:
                    fk_crit = {'pk':int(v)}
                new_fk_obj = fk_m.objects.get(**fk_crit)
                v = new_fk_obj                
            if m._meta.get_field(k).unique \
            and 0 < m.objects.filter(**{k:v}).count() < 2:
                c_ = self.utils.c_io(
                        self.utils.get_conf_model_mix(
                        self.c['form']['elements'],
                        self.model)
                )['d']
                if k in c_ \
                and 'readOnly' in c_[k]: 
                    pass
                else: 
                    r['errors'].append('Väärtus %s on andmebaasis juba olemas' % v)
            elif k:
                to_db_d[k] = v \
                    if not v in ('none','Null','') \
                    else None
            if ft == 'DecimalField':
                if k in to_db_d: 
                    del to_db_d[k]
                        
            u = self.request.sarvuser.username
            from datetime import datetime
            try:
                m._meta.get_field_by_name('user_changed')
                to_db_d.update({
                    'user_changed': u,
                    'date_changed': datetime.now()})
            except: 
                pass
            try:
                #if there's one, there are others
                m._meta.get_field_by_name('user_modified')
                to_db_d.update({
                    'user_modified': u,
                    'timestamp_modified': datetime.now()})
            except: 
                pass
            
            try:
                m_ = m.objects.filter(pk=post['id'])
                m_.update(**to_db_d)
            except Exception as e:
                r['errors'].append(str(e))
            
            r.update({'success': True \
                      if len(r['errors']) < 1 \
                      else False})
        return HttpResponse(json.dumps(r),
                    content_type="application/json")
    
    def delete_record (self):
        get = self.request.GET.dict()
        idr = get['id']
        r={'errors':[], 
           'response':[]}
        
        '''
        1. Request to delete grid in a form
        '''
        if 'gridname' in get:
            g = get['gridname']
            g_d = self.utils.c_io(
                    self.utils.get_conf_model_mix(
                        self.c['form']['elements'],
                        self.model)
            )['d'][g]

            if 'model' in g_d:
                model = self.get_model(g_d['model'])
                qs = model.objects.get(pk=idr)
                if not self.cclear_reverse_relationships(qs, 
                model) == 'has relations':
                    r['response'].append('success')
                    qs.delete()
                else: 
                    r['errors'].append('Leidub kirjega seotud kirjeid') #response = 'has relations'
            return HttpResponse(json.dumps(r),
                                content_type="application/json")

        '''
        2. Request to delete a form
        '''
        if self.utils.is_int(idr):
            qs = self.model.objects.get(pk=idr)
            if not self.cclear_reverse_relationships(qs, 
            self.model) == 'has relations':
                try:
                    qs.delete()
                except Exception as e:
                    r['errors'].append(str(e))
            else: 
                r['errors'].append(
                    'Leidub kirjega seotud kirjeid')
        r.update({
            'success': True \
                if len(r['errors']) < 1 \
                else False })
        return HttpResponse(json.dumps(r),
                            content_type="applicaton/json")
    
    def clear_reverse_relationships (self, recordset):
        for related in self.model._meta.get_all_related_objects():
            accessor = related.get_accessor_name()
            related_set = getattr(recordset, accessor)

            if related.field.null:
                related_set.clear()
            else:
                for __ in related_set.all():
                    self.clear_reverse_relationships(recordset)

    def cclear_reverse_relationships (self, recordset, model):
        for related in model._meta.get_all_related_objects():
            accessor = related.get_accessor_name()
            related_set = getattr(recordset, accessor)
            if related_set.count() > 0:
                return 'has relations'
