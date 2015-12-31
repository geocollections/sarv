#from sarv.models import *

class Ordered(object):
    """
    Class to replace OrderedDict in py3. 
    Used in config.py filter definitions.
    """
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
