from django.apps import apps
from django.conf import settings

# Load source app from various apps
# Caveat: Either loaded model classes have no app_label
# or app_label must be named after app name. Conflicting
# app_label creates error.

def get_model (*args):
    # Select app name
    if hasattr(settings, "MODEL_APP") \
    and settings.MODEL_APP in settings.INSTALLED_APPS \
    and len(args) < 2:
        app_name = settings.MODEL_APP
    elif len(args) == 2:
        app_name = args[0]
    else:
        app_name = "nextify"

    if app_name.startswith("apps."):
        app_name = app_name.replace("apps.", "")
    model_name = args[0] if len(args) < 2 else args[1]
    
    if isinstance(model_name, (list, tuple)):
        classes = []
        for i in model_name:
            classes.append(apps.get_model(
                app_name, i
            ))
        return classes
    else:
        return apps.get_model(
            app_name, model_name
        )
