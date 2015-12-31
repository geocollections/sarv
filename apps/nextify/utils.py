# -*- coding: utf-8 -*-

from functools import reduce
import operator as join_operator

from django.db.models import Q
from django.conf import settings
from django.apps import apps

from apps.nextify.config import (
    Page, 
    PageElement as PaEl, 
    Filter, 
    Form, 
    MODELS_WITH_REMOTE_STORES
)

class NextifyUtils(object):
    def __init__(self, defaults = None):
        self.input = defaults
        self.qs=None
        self.n=0
        self.fk_d={}
                   
    
    def get_model (self, mname = None):
        """
        Get model instance by name
        and include database parameter.
        
        @param mname: Model name
        @type mname: str
        """
        if not 'request' in self.input:
            print('fatal error in NextifyUtils.get_model')
        if not mname:
            pass

        from sarv.utils import get_model
        m = get_model(mname)
        s = self.input['request'].session
        if 'database_id' in s \
        and isinstance(s['database_id'], int) \
        and hasattr(m, 'session_db'):
            m.session_db = s['database_id']
        return m
    
    def get_url_list (self):
        """
        Returns list of page names specified in config.py
        Page object as object property names. 
        
        @rtype: list
        """
        out = []
        for k,v in Page.__dict__.items(): 
            if not (k.startswith('__') \
            and k.endswith('__')) \
            and not callable(v):
                out.append(k) 
        return out
    
    def get_filters_list (self):
        """
        Returns list of filter types
        specified in config.py Filters object.
                
        """
        out = {}
        for k,v in Filter.__dict__.items():
            if not (k.startswith('__') \
            and k.endswith('__')) \
            and not callable(v) \
            and not k == 'types': 
                out[k]=[[i[0], i[1]] for i in v]
        return out
    
    def get_urlpatterns (self):
        """
        Returns list of Django urls patterns 
        created from config.py Page property names
        """
        from django.conf.urls import patterns
        out = []
        for i in self.get_url_list():
            try:
                out += patterns('', 
                        (r"^%s/" % i, 
                        'apps.nextify.views.index', 
                        {'page':i}
                ))
            except:
                print('Aadressi laadimine ebaõnnestus')
        return out
    
    def get_fields_list (self):
        pass
    
    def is_int(self, *args):
        """
        Test if given argument is integer
        
        @param args: List of arguments
        @type args: list
        @rtype: bool
        """
        out=False
        try:
            int(args[0])
            out=True
        except:
            pass
        return out
    
    def c_io(self, g_l):
        """
        Primary interpretor of config definitions
        
        @param i_l: Given config nested dict
        @type i_l: 
        
        """
        i_l = self.el_to_item(g_l)
        out={'d':{},'l':[]}
        
        # fix to allow all-fields inclusion:
        # 1.If list is encapsulated with one pair of list brackets
        # then all model fields are included and those given
        # inside brackets are presented in their respective positions (?)
        # 2.If list is encapsulated with two pairs of list brackets
        # show only these fields 
        
        zo_l=[]
        def c_rec(i, o_d, o_l, n, zor_l):
            if isinstance(i, list) \
            and isinstance(i[-1:][0], dict): 
                # dict - element properties, list - flat list of elements
                if len(i) > 2:
                    # [[], .., {}]
                    for j in i[:-1]:
                        if isinstance(j, list):
                            o_d,o_l,n,zor_l=c_rec(j,o_d,o_l,n, zor_l)
                        else:
                            o_l.append(j)
                            zor_l.append(j)
                    o_d.update({'hbox-'+n:i[-1:]})
                    o_l.append('hbox'+n)
                    n+=1
                else:
                    # [[], {}]
                    o_d.update({i[0]:i[1]})
                    o_l.append(i[0])
                    zor_l.append(i[0])
            elif isinstance(i, (list, tuple)):
                if n==0:
                    zor_l=[]
                for a in i:
                    o_d, o_l, n, zoz_l=c_rec(a, o_d, o_l, n,zor_l)
                    if n==1:
                        zor_l.append(zoz_l)
                if n==0:
                    zo_l.append(zor_l)
                    
            elif isinstance(i, dict):
                o_d.update(i)
            else: # String
                o_d.update({i:{}})
                o_l.append(i)
                zor_l.append(i)
            return o_d,o_l,n,zor_l
        
        out['d'], out['l'], __, __=c_rec(i_l, {}, [], 0, []) 
        out.update({'z':zo_l})
        return out

    def get_conf_model_mix(self, conf, model):
        strict = len(conf) == 1
        if strict:
            return conf[0]
        c=self.c_io(conf)
        f_l=c['l']
        f_sl=c['z']
        row=0
        p_d={}
        for i in model._meta.fields:
            if i.name in ['id','user_added','user_changed','database']:
                continue
            if i.name in f_l:
                # find it in structured config
                for m,r in enumerate(f_sl):
                    if (isinstance(r, str) and i.name==r) \
                    or (isinstance(r, list) and i.name in r):
                        if m > row:
                            row=m
                        break
            else:
                if not row in p_d:
                    p_d.update({row:[]})
                p_d[row].append(i.name)
        p_l=[]
        # Add extra elements to cf.
        for n,i in enumerate(conf):
            p_l.append(i)
            if n in p_d:
                for j in p_d[n]:
                    p_l.append(j)
        return p_l

    def copy_model_fields (self):
        """
        
        """
        for f in self.model._meta.fields:
            if f.name == 'database':
                continue
            self.fields.update({
                f.name:f})
    
    def xtype_radio(self, f):
        """
        
        """
        out = []
        txt = {None: 'Pole valitud',
                True: 'Jah',
                False: 'Ei'}
        for i in (None, True, False):
            r={
               'name': f,
               'boxLabel': txt[i],
               'inputValue': i
            }
            if i==None:
                r.update({'checked': True})
            out.append(r)
        return out
    
    def model_f_to_ext (self, f, c):
        """
        
        """
        qs=self.qs
        if not f in self.fields:
            return
        
        mf=self.fields[f]
        mft=mf.get_internal_type()
        fk=True if mft=='ForeignKey' else False
        relm = self.model._meta.get_field(f).rel.to \
            if fk else None
        ''' value '''
        out={}
        v=None
        out.update({'fieldLabel': mf.verbose_name,
             'flex': 1,
             'padding': 5,
             'value': None, 
             'sarv': {},
             'vtype': ''})
        if not qs: # 1. If form is empty
            pass
        elif mft in ('DateField','DateTimeField','TimeField'):
            if mft=='DateTimeField':
                v=str(getattr(qs, f)).split(' ')[0]
            else:
                v=str(getattr(qs, f))
        elif fk:
            rfs=[i.name for i in relm._meta.fields]
            l=rfs[0 if rfs[0]!='id' else 1]
                
            if not 'fk_label' in c['sarv']:
                c['sarv'].update({'fk_label':{settings.LANGUAGE_CODE:l}}) 
            v = getattr(qs, f+'_id') \
                if hasattr(qs, f+'_id') else 0 
        else:
            v=getattr(qs, f)
        if fk:
            ''' combo store model '''
            out['sarv'].update({
                'store_model': relm.__name__.lower(),
                'store_type': 'local'
            })
            ''' Remote store '''
            if mf.rel.to.__name__ \
            in MODELS_WITH_REMOTE_STORES:
                f_d=self.get_store_model_fields(
                    self.model, f, c, settings.LANGUAGE_CODE)
                
                vf=f+'__' 
                vf+=f_d['value_field']
                
                out['sarv'].update({
                    'store_type':'remote',
                    'store_default_field':vf,
                    'xtype':'sarv-field-combo-remote'
                })
            
            if 'store_type' in c:
                out['sarv'].update({
                    'store_type': 
                    c['store_type']})
            
            ''' clickable '''
            if self.model == relm \
            and hasattr(qs, f):
                out['sarv'].update({'href':''})
                if getattr(qs, f): 
                    url={'url': getattr(qs, f+"_id")}
                    out['sarv'].update(url)
            
            ''' default combo values '''            
            if qs:
                if not 'defaults' \
                in out['sarv']:
                    out['sarv'].update({'defaults':[]})
                try:
     
                    out['sarv']['defaults']={
                        #'name': v if v else '',
                        'value': getattr(qs, f+"_id") \
                            if getattr(qs, f+"_id") else '',
                    }
                except:
                    pass

            #''' Add form combobox_size config '''
            if 'pageSize' in c:
                out['sarv'].update({'pageSize':c['pageSize']})
            elif 'combobox_size' in self.c['form']:
                out['sarv'].update({'pageSize':self.c['form']['combobox_size']})
            
            ''' Link button to grid rows '''
            if 'model' in c:
                url_to_form = [url for url in self.utils.get_url_list() \
                    if hasattr(Page, url) \
                    and 'model' in getattr(Page, url) \
                    and getattr(Page, url)['model'] == \
                    relm.__name__]
                if len(url_to_form) > 0:
                    out['sarv'].update({'urlpart': url_to_form[0]})

        elif f == 'owner': 
            pass
        
        if hasattr(Form, 'readonly') \
        and f in Form.readonly:
            out.update({'readOnly':'true'}) 
        if hasattr(mf, 'decimal_places') \
        and not 'decimal_places' in c:
            out.update({'decimalPrecision:':
                        mf.decimal_places})
        if mft == 'BooleanField':
            out.update({'checkedValue': True,
                        'uncheckedValue': False})
            if out['value']!='': 
                out.update({'checked':'true'})
        if not v:
            v=''

        out.update({'value':v})
        if not mf.blank:
            out.update({'allowBlank': False})
        return out


    def typify (self, f, c={}):
        """
        Transform given field config in conjunction 
        with model definition into ExtJS config format
        
        @type f: string
        @param f: Field name (typically a model name)
        @type c: dict
        @param c: Config dict for this field
        @rtype: dict
        @return: Field config in ExtJS format 
        """
        
        if not self.fields:
            self.copy_model_fields()
         
        if f=='hbox':                           # 1. Nesting
            out={}
            for k,v in c.items():
                out.update({k:v})
            
            out.update({
                'xtype':'sarv-hbox',
                'name':'sarv-hbox-'+str(self.n),
            })
            self.n+=1

        elif f.startswith('grid_'):             # 2. Grid
            out={
                'xtype': 'sarv-grid-panel',
                'name': f,
                'id': 'sarv-grid-'+f,
                'title': c['title'],
                'columns': [],
            }
            
            if 'pagesize' in c:
                out.update({
                    'pageSize': c['pagesize']
                })

            ''' flags to grid column fields '''
            gf=[{'sarv-grid-columns': True}]
            m=self.get_model(c['model'])
            for i in c['fields'][0]:
                f_n=i if isinstance(i, str) else i[0]
                if '__' in f_n:
                    f_n=f_n.split('__')[0]
                
                rf=m._meta.get_field(f_n) 
                rfk=True if rf.get_internal_type() \
                    == 'ForeignKey' else False
                
                flag={'xtype': 'sarv-grid-field',
                      'text': rf.verbose_name
                }
                
                if hasattr(Form, 'readonly') \
                and rf.name in Form.readonly:
                    flag.update({'readonly': True})
                                
                if hasattr(rf, 'blank') \
                and not rf.blank:
                    flag.update({
                        'allowBlank': False})
                
                if isinstance(i, list) \
                and isinstance(i[1], dict):
                    flag.update(i[1])
                                
                if rfk:
                    sm=rf.rel.to.__name__
                    st=None
                    vf=None
                    if sm in \
                    MODELS_WITH_REMOTE_STORES:
                        st='remote'
                        vf=rf.name+'__' \
                            if not sm == \
                            m.__name__ \
                            else ''
                        # c - is grid conf. 
                        vf+=self.get_store_model_fields(
                            m, rf.name, 
                            i[1] if isinstance(i, list) \
                            and len(i) == 2 else {}, 
                            settings.LANGUAGE_CODE)['value_field']
                    flag.update({
                        'sarv-type': 'combo',
                        'sarv':{
                            'store_model': sm.lower(),
                            'store_type': st
                    }})
                    if vf:
                        flag['sarv'].update({
                            'store_default_field':vf
                        })
                    

                if rf.get_internal_type() == 'BooleanField':
                    flag.update({
                        'sarv-type': 'checkcolumn'})
                
                if rf.get_internal_type() == 'NullBooleanField':
                    out.update({
                        'sarv-type': 'radiocolumn',
                        'items': self.xtype_radio(f)
                    })
                
                if isinstance(i, str):
                    gf.append([i, flag])
                elif len(i)==2 \
                and isinstance(i[1], dict):
                    i[1].update(flag)
                    gf.append(i)
            
            out.update({'columns':
                        self.reconf(gf)})
            
            ''' Link button to grid '''
            urlb=[url for url in self.get_url_list() \
                    if hasattr(Page, url) \
                    and 'model' in getattr(Page, url) \
                    and getattr(Page, url)['model'] == \
                    m.__name__]
            if len(urlb) > 0:
                out['columns'].insert(0, {
                    'sarv-type': 'actioncolumn',
                    'width': 20,
                    'sarv': {'urlpart': urlb[0]}
                })
            
        elif 'xtype' in c \
        and c['xtype'] == 'sarv-grid-field':    # 3. Grid columns
            out={}
            for k,v in c.items():
                out.update({k:v})
            
            # If invalid spelling of 
            # readonly in config, correct it
            if 'readonly' in out:
                out.update({'readOnly':
                    out['readonly']})
                del out['readonly']
            
            # Stretching the grid when necessary
            if not 'width' in out:
                out.update({'flex':1}) 
            out.update({
                'dataIndex': f if not f=='id' else 'id_',
            })
            if 'xtype' in out:
                del out['xtype'] 
        elif f == 'tab':                        # 4. Tab
            out = {
                'xtype': 'sarv-tab',
                'name': 'sarv-tab-'+str(self.n),
                'activeTab':0
            }
            for k,v in c.items():
                out.update({k:v})
            
            self.n+=1

        elif isinstance(f, str):                # 6. Simple 
            fk=False
            out={'name': f,'labelAlign':'right'}
            if f in self.fields:
                mf=self.fields[f]
                mft=mf.get_internal_type()
                fk= True if mft == 'ForeignKey' \
                    else False
                
                if hasattr(mf, 'blank') \
                and not mf.blank:
                    out.update({'allowBlank':False})
            
                if mft=='NullBooleanField': # - radio
                    out.update({
                        'xtype': 'sarv-field-radio',
                        'items': self.xtype_radio(f)
                    })
                elif mft=='BooleanField':
                    out.update({
                        'xtype': 'sarv-field-checkbox'})
                elif fk:
                    out.update({
                        'xtype': 'sarv-field-combo',
                        'cls': 'sarv-field-combo'
                    })
                    
                    ''' Remote store '''
                    if mf.rel.to.__name__ \
                    in MODELS_WITH_REMOTE_STORES:
                        f_d=self.get_store_model_fields(
                            self.model, f, c, settings.LANGUAGE_CODE)

                        vf=f+'__' \
                            if not mf.rel.to.__name__ == \
                            self.model.__name__ \
                            else ''
                        vf+=f_d['value_field']
                        out.update({
                            'store_type':'remote',
                            'store_default_field': vf,
                            'xtype':'sarv-field-combo-remote'
                        })
          
                    if not f in self.fk_d:
                        mn=self.model.__name__#.lower()
                        if not mn in self.fk_d:
                            self.fk_d.update({mn:[]})
                        self.fk_d[mn].append(f)
                elif 'file' in c:
                    out.update({
                        'xtype':'sarv-file',
                    })
                else:
                    out.update({'xtype': 
                        Form.field_types[ mft ]})
                    
                if mft in ('DateField','DateTimeField'):
                    out.update({'format':
                        'Y-m-d'})
            
            ''' column '''
            # Needs to be optimized -
            # is this method necessary?
            fc=self.model_f_to_ext(f, c)
            
            if isinstance(fc, dict):
                out.update(fc)
            for k,v in c.items():
                if k=='resizable' \
                and 'xtype' in out \
                and out['xtype']=='textareafield' \
                and v:
                    if not 'fieldCls' in out:
                        out.update({
                            'fieldCls':'resizableTextArea'})
                    else:
                        out['fieldCls']+=' resizableTextArea'
                    continue 
                out.update({k:v})
        return out
    '''
    [
    <fieldname>,
    [<fieldname>,<fieldname>,[<fieldname>,<fieldname>] ],
    [<fieldname>, {config}]
    
    ]
    @param f - field
    '''
    def reconf (self, f):
        """
        Nextify form field item interpreter.
        Nextify form config consists of field
        definitions that attempt to be as 
        efficient in their expression as possible.
        
        @type f: mixed
        @param f: Field config item
        """
        out=None
        if isinstance(f, str):
            if f.startswith('.'):
                
                # 1. Page element
                # Get related config before new i_conf
                i=self.el_to_item(f)
                out=self.typify(i[0], i[1])
            else:
                
                # 2. Field name 
                out=self.typify(f)
        elif isinstance(f, (list,tuple)):
            if len(f) == 2 \
            and isinstance(f[1], dict):
            
                # 3. Field name and config dict
                out=self.typify(f[0], f[1])
            else:
                
                # 4. List of nested items or grid columns or tab panel - if tuple
                j=[]
                c={}
                for i in f:
                    # Nesting field could contain
                    # config dict. Example:
                    # [<f>,<f>,{c}]
                    if isinstance (i, dict):
                        c.update(i)
                    else:
                        j.append(self.reconf(i))
                # For grid columns no hbox
                if 'sarv-grid-columns' in c:
                    out=j
                elif isinstance (f, tuple):
                    c.update({'items':j})
                    out=self.typify('tab', c)
                else:
                    c.update({'items':j})
                    out=self.typify('hbox', c)
        return out 
    
    def el_to_item (self, l):
        """
        Checks recursively whether provided element 
        in config list is page element (marked with 
        punctuation in front of item key. When finding 
        transforms into a field. 
        """
        if not 'page' \
        in self.input: 
            return
        out=[]
        if not isinstance(l, (str, dict)):
            for i in l:
                j=[self.el_to_item(i[0]), i[1]] \
                    if len(i) > 1 \
                    and isinstance(i[1], dict) \
                    else self.el_to_item(i)
                out.append(j)
        elif isinstance(l, str):
            p=self.input['page']
            n=p+'_'+l[1:]
            if not l.startswith('.'): 
                out = l
            elif hasattr(PaEl, n):
                out = getattr(PaEl, n)
            elif hasattr(PaEl, l[1:]):
                out = getattr(PaEl, l[1:]) 
        return out 


    def get_q_uery (self, f_d):
        """
        @summary: Compose Django Q query from provided dict
        
        @param f_d: Query filter params
        @type f_d: dict
        """
        if len(f_d) < 1: 
            return
        r = []
        for k,v in f_d.items():
            if k in ('Or','And'):
                for i in v:
                    r.append(self.get_q_uery(i))
            elif isinstance(k, str):
                k_=list(v.keys())[0]
                kw_d = {k+'__'+k_: v[k_]}
                r.append(Q(**kw_d))
        return reduce(join_operator.or_ \
                    if k == 'Or' \
                    else join_operator.and_, 
                r)
    
    def get_stores_fields_list(self, c_d, gs_b, model):
        '''
        @summary: Get all store fields for particular page
            Used by get_stores() and get_everything()
            Fields are in self.utils.fk_l
            gs_b - (bool) add also grid store fields
        
        @type c_d: dict
        @param c_d: config dict
        @type gs_b: bool
        @param gs_b:
        @rtype: 
        @return: none
        '''
        c = self.c_io(self.get_conf_model_mix(c_d['form']['elements'], model))#c_d['form']['elements'])
        
        for k in c['l']:
            if k.startswith('grid_'):
                if gs_b:
                    mn=c['d'][k]['model']
                    rc=self.c_io(
                        c['d'][k]['fields'][0]
                    )['l']
                    ''' Iterate over grid items listed '''
                    rm=self.get_model(mn)
                    for i in rc:
                        rf=rm._meta.get_field_by_name(i)[0]
                        if rf.get_internal_type() == 'ForeignKey' \
                        and (not mn in self.fk_d \
                        or not i in self.fk_d[mn]):
                            if not mn in self.fk_d:
                                self.fk_d.update({mn:[]})
                            self.fk_d[mn].append(i)                          
            else:
                m=self.model
                try:
                    mn_=m.__name__
                    f=m._meta.get_field_by_name(k)[0]
                    if f.get_internal_type() == 'ForeignKey':
                        if not mn_ in self.fk_d:
                            self.fk_d.update({mn_:[]})
                        if not k in self.fk_d[mn_]:
                            self.fk_d[mn_].append(k) 
                except:
                    continue

    def get_store_model_fields(self, m, f, c_di, l):
        """
        @summary: Get model fields that are used as displayfields in
            form dropdown (ext combobox) selectors. These fields
            are defined in config.py. If a field is not defined
            in config, first field in model - that is not primary
            key - is used.
        
        @type m: Dj. model obj
        @param m: Field model
        @type f: string 
        @param f: Field name
        @type c_d: dict
        @param c_d: Field config dict,
        @type l: string 
        @param l: Language code ("ee","et",..) 
        """
        c_d={k:v for k,v in c_di.items()}
        try:
            fk_m = m._meta.get_field(f).rel.to
        except:
            return None
        l = (l or settings.LANGUAGE_CODE)

        # When a fk_label conf is not found.
        # Set one by using the first field of model
        if not 'fk_label' in c_d:
            if not hasattr(settings, "DEBUG") \
            or settings.DEBUG:
                print ('''[nextify.utils.get_store_model_fields] combobox display field not defined in config.py for "%s". Inserting first field after pk.''' % f)
            rf_l = [i.name for i in fk_m._meta.fields]
            n = rf_l[1 if rf_l[0] == 'id' else 0]
            c_d.update({
                'fk_label':{l:n}
            })
        vf = c_d['fk_label'][l]
        nf = m._meta \
                .get_field(f) \
                .rel.field_name
        
        return {
            'name_field': nf,
            'value_field': c_d['fk_label'][l],
            'm': fk_m,
            'c_d': c_d
        }
