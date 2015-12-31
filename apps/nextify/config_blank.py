# -*- coding: utf-8 -*-
"""
Configuration file.
"""

class Page (object):

    issue = {
        'model': 'SarvIssue',
        'grid_default': 'my',
        'filters_disabled': [],
        'filters_default': [{'title':0}, {'description':0}],
        'fields': [
            ['id', {'width':60}],
            ['issue_type__issue_type',{'width':100}],
            ['title',{'width':300}],
            ['resolved',{'width':50}],
            ['reported_by__username',{'width':70}],
            ['reported_to__username',{'width':70}],
            ['date_added',{'width':140}]
        ],
        'pagesize': 100,
        'form': {
            'title': '{{title}}',
            'window': {'width': 400, 'height': 600},
            'combobox_size': 10,
            'elements': [
                ['description'],
                'url',
                ['response'],
                ['resolved'],
                [['user_added',{'width':200}], ['date_added',{'width':200}]],
                [['user_changed',{'width':200}], ['date_changed',{'width':200}]],
            ]
        }
    }

"""
Re-usable page element configuration class.
"""
class PageElement(object):
    pass

    #locality_grid_locality = ["grid_parent", {
    #    "model": "LocalityReference",
    #    "related_field": "parent",
    #    "fields": ["reference","id","remarks"],
    #    "pagesize": 5
    #}]

# Django models that when used as models
# are defined as remote comboboxes in ExtJS form
MODELS_WITH_REMOTE_STORES = []

"""
System configuration. 
"""
class Ordered(object):
    d={}
    l=[]
    def __init__(self, l):
        self.d={}
        self.l=[]
        if len(l) < 1 \
        or not isinstance(l, list):
            return
        for i in l:
            self.l.append(i)
        self.d=dict(l)

    def __len__(self):
        return len(self.l)

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.l[i]

    def value_for_index(self, i):
        if len(self.l) > i:
            return self.l[i][1]

class Filter (object):
    string = Ordered([
        ('icontains', 'sisaldab'),
        ('exclude_icontains', 'ei sisalda'),
        ('iexact', 'võrdub'),
        ('istartswith', 'algab'),
        ('iendswith', 'lõpeb')
    ])
    
    numeric = Ordered([
        ('exact', 'võrdub'),
        ('exclude_iexact', 'ei võrdu'),
        ('gt', 'suurem kui'),
        ('lt', 'väiksem kui')
    ])
    
    boolean = Ordered([
        ('exact', 'on')
    ])
    
    nullboolean = Ordered([
        ('exact', 'on')    
    ])
    
    
    types = {
        'CharField': 'string',
        'TextField': 'string',
        'IntegerField': 'numeric',
        'FloatField': 'numeric',
        'DecimalField': 'numeric',
        'DateTimeField': 'numeric',
        'DateField': 'numeric',
        'ForeignKey': 'string',
        'BooleanField': 'boolean',
        'NullBooleanField': 'nullboolean',
        'AutoField': 'numeric' # 'id' in models
    }
    
class Form (object):
    
    # Django field type to ExtJS field type
    field_types = {
        'CharField': 'textfield',
        'TextField': 'textareafield',
        'IntegerField': 'numberfield',
        'FloatField': 'numberfield',
        'DecimalField': 'numberfield',
        'DateTimeField': 'textfield',
        'DateField': 'datefield',
        'ForeignKey': 'combo',      
        'BooleanField': 'checkbox',
        'NullBooleanField': 'radiogroup',
        'AutoField': 'numberfield'
    }
    
    # read-only fields
    readonly = ('timestamp',
                'date_added',
                'date_changed',
                'id',
                'user_added',
                'user_changed',
                'id_')
