# Django settings for sarv project.
import os

DEBUG = True # ! 28.10
TEMPLATE_DEBUG = DEBUG
#ADMINS = () # Defined in local_settings.py
#ALLOWED_HOSTS = [] # Defined in local_settings.py
PROJECT_DIR = os.path.dirname(__file__)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Tallinn"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, "static/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = "/media/"

# Make this unique, and don"t share it with anybody.
SECRET_KEY = ""

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    "django.template.loaders.filesystem.load_template_source",
#    "django.template.loaders.app_directories.load_template_source",
#     "django.template.loaders.eggs.load_template_source",
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

#TEMPLATE_CONTEXT_PROCESSORS = (
#    "django.core.context_processors.request",
#    "django.contrib.auth.context_processors.auth"
#)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    "sarv.middleware.IDAuthSessionMiddleware", # uncomment this to enable ID card authentication
    "apps.acl.middleware.PageRightsCheck",
)

ROOT_URLCONF = "sarv.urls"

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR,"templates"),
    os.path.join(PROJECT_DIR,"sarv","templates"),
    os.path.join(PROJECT_DIR,"..","apps","menu","templates"),
    os.path.join(PROJECT_DIR,"..","apps","nextify","templates"),
    os.path.join(PROJECT_DIR,"..","apps","custom","templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "apps.acl",
    "apps.menu",
    "apps.nextify",
    "apps.custom",
    "sarv"
]

STATIC_URL = "/static/"


SESSION_COOKIE_AGE = 3600 # session expires after 1 hour of inactivity
SESSION_SAVE_EVERY_REQUEST = True

DATE_INPUT_FORMAT = "%d/%m/%Y"
DATETIME_INPUT_FORMAT = "%d/%m/%Y H:i:s"

#from django.db import connections
DATABASE_ROUTERS = [
    "sarv.routers.DatabaseRouter",
    #"apps.nextify.routers.DatabaseRouter", # This needs to be addressed
]

MODEL_APP = "apps.nextify"

from sarv.local_settings import *

# If model in module outside current Django project is used:
# ---------------------------------------------------------
# 1. Add its location in filesystem to PYTONPATH for example in Apache WSGIDaemonProcess
# 2. Add its module name to INSTALLED_APPS right before "sarv" app (second last)
# 3. Define MODEL_APP config parameter as string with name of module that holds models.py file

"""
Properties defined in local_settings.py
ADMINS = ()
ALLOWED_HOSTS = [] # If DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": "", # your db name
        "USER": "", # your db username
        "PASSWORD": "", # your db password
        "HOST": ""
    },
    "sarv": {
        "ENGINE": "mysql.connector.django",
        "NAME": "", # your db name
        "USER": "", # your db username
        "PASSWORD": "", # your db password
        "HOST": ""
    }
}

NEXTIFY_DOWNLOAD_DIR = "" # File download directory

PUBLIC_STATIC_URL = "/public/"

USER_DATABASE = "users"

ACL_USERLEVELS = ("guest","user","editor","admin") # No need to change this

# Map which userlevel has which right
ACL_USERRIGHTS = [
    [False,False,False,False],
    [True,False,False,False],
    [True,True,"own","own"],
    [True,True,True,"own"],
    [True,True,True,True]
]

PROJECT_ADMINS = [] # Project admin user id list
"""

MANAGERS = ADMINS
