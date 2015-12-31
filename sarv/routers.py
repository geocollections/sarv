from django.conf import settings

def db_for_model(model):
    if model._meta.app_label in ["nextify", "acl"]:
        return "sarv"
    models = __import__("%s.models" % settings.MODEL_APP, globals(), locals(), [model.__name__])
    if hasattr(models, model.__name__) \
    and model._meta.db_table != "auth_user": 
        return "sarv"
    else:
        return "default" # connection to django db

class DatabaseRouter(object):

    def db_for_read(self, model, **hints):
        return db_for_model(model)

    def db_for_write(self, model, **hints):
        return db_for_model(model)

    def allow_migrate(self, db, model):
        if db == "sarv" and not db_for_model(model) == "sarv" \
        or not db == "sarv" and db_for_model(model) == "sarv":
            return False
        return True
