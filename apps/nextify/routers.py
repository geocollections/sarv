class DatabaseRouter(object):
    """A router to control all database operations on models in
    the nextify application"""
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'nextify':
            return 'sarv'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'nextify':
            return 'sarv'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'nextify' \
        or obj2._meta.app_label == 'nextify':
            return True
        return None
    
    def allow_syncdb(self, db, model):
    
        if db == 'sarv':
            return model._meta.app_label == 'nextify'
        elif model._meta.app_label == 'nextify':
            return False
        return None
